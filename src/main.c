/* main.c -- the scheduler and the glue, and deliberately nothing else.
 *
 * Every number this device puts on the bus is computed by the pure core, which
 * knows nothing about the PIC; everything that touches a register is in
 * hal_can.c or hal_sys.c. This file is the only place the two meet, and it is
 * short on purpose -- if arithmetic ever appears here, it is in the wrong file
 * and it has stopped being testable on a PC.
 *
 * A cooperative scheduler on one free-running millisecond clock. No RTOS, no
 * priorities, nothing that can deadlock.
 *
 *    every pass   drain the CAN receive FIFO, offer the clock to the core
 *                 (which integrates distance on its own DIST_TICK_MS step)
 *    every 25 ms  one transmit slot, and AT MOST ONE FRAME in it -- 0x600,
 *                 0x601, 0x602, 0x603, and the EEPROM in a slot that sends
 *                 nothing. config.h has the measurement that forced that.
 */
#include "pic_config.h"     /* #pragma config ... and then <xc.h> */

#include <stdbool.h>
#include <stdint.h>

#include "compute.h"
#include "config.h"
#include "decode.h"
#include "hal_can.h"
#include "hal_sys.h"
#include "persist.h"
#include "txframes.h"

/* File scope rather than automatic: compute_t alone is a few hundred bytes of
 * windows and history, and XC8's compiled stack is not the place for it. */
static decode_state_t st;
static compute_t      cp;
static persist_t      ps;
static tx_values_t    tx;

/* --- the LEDs ------------------------------------------------------------ */

/* Both are dark unless the DBG_EN jumper is fitted -- hal_sys enforces that,
 * not this file -- so nothing lights up in the car.
 *
 *   LED_PWR   steady        the loop is running and we are on the bus
 *             slow blink    the loop is running but the module is in one of
 *                           the silent modes, so nothing is being transmitted
 *   LED_CAN   steady        frames are arriving and the module is healthy
 *             2.5 Hz blink  arriving, but an error counter is not zero or the
 *                           FIFO has just overflowed
 *             5 Hz blink    hal_can_init() never got the module into the mode
 *                           it asked for; there is no CAN at all
 *             off           the bus has been quiet for DATA_TIMEOUT_MS
 *
 * The distinction that matters on a bench is the last two: dark means the car
 * is not talking, fast blink means we are not listening.
 *
 * THE 2.5 Hz BLINK IS THE LIVE FAULT AND NOT THE LATCHED ONE. The module's
 * error counters come back to zero on their own once the bus behaves, so this
 * light goes out again when the trouble stops -- config.h argues why that is
 * the right half to show. What it does NOT do is remember, and that is the
 * other flag's job: DIAG_FLAG_UNHEALTHY in 0x603 stays set for the rest of the
 * session and is the only thing that can say something happened while nobody
 * was watching.
 *
 * LED_PWR carries the silent modes because a listen-only build is otherwise
 * indistinguishable from a broken transmitter -- frames arrive, LED_CAN is
 * steady, the display shows nothing, and there is no way to tell from the
 * outside that it is doing exactly what it was built to do. */
static void leds_update(bool can_ok, bool live, bool unhealthy, uint8_t phase)
{
    bool on;

    if (!can_ok) {
        on = (phase & 0x01u) == 0u;         /* 5 Hz   */
    } else if (!live) {
        on = false;
    } else if (unhealthy) {
        on = (phase & 0x03u) < 2u;          /* 2.5 Hz */
    } else {
        on = true;
    }

    /* phase advances every TX_FAST_MS, so 0x07 is a 0.8 s half-period. */
    hal_sys_led_pwr(hal_can_silent() ? ((phase & 0x07u) < 4u) : true);
    hal_sys_led_can(on);
}

/* --- the diagnostic frame ------------------------------------------------ */

/* Every refusal by hal_can_send() since power-up, saturating. It counts rather
 * than latches because the number distinguishes two different faults: a
 * handful means the three transmit buffers were briefly all busy, which is
 * survivable and expected under arbitration, while a count that tracks the
 * uptime means nothing is getting out at all. */
static uint8_t tx_fail = 0u;

/* An overflow this firmware caused itself, by blocking on an EEPROM write, is
 * not a fault to report -- see the write slot. It cannot be forgiven where it
 * happens, though: clearing the flag while the FIFO is still full only lasts
 * until the next frame arrives into it, which at the bench's frame rate is a
 * millisecond away. So the write raises this, and the forgiveness happens on
 * the next pass, AFTER the drain has emptied the FIFO. An arriving frame
 * cannot overflow an empty FIFO, so there is no window left. */
static bool pardon_overflow = false;

static void tx_fail_count(void)
{
    if (tx_fail < 0xFFu) {
        tx_fail++;
    }
}

static uint8_t diag_flags(bool can_ok, bool unhealthy, bool unhealthy_now,
                          bool persist_ok, bool live)
{
    uint8_t f = 0u;

    if (can_ok) {
        f |= DIAG_FLAG_CAN_OK;
    }
    /* Only loopback can reach this line while silent: listen only transmits
     * nothing, so a 0x603 that arrives with this bit set came from a loopback
     * build talking to itself. */
    if (hal_can_silent()) {
        f |= DIAG_FLAG_SILENT;
    }
    if (unhealthy) {
        f |= DIAG_FLAG_UNHEALTHY;
    }
    /* The live half, which is what LED_CAN follows. Both are here on purpose:
     * one says a fault is happening, the other that one ever did, and telling
     * those apart is the difference between a lead and a shrug. */
    if (unhealthy_now) {
        f |= DIAG_FLAG_UNHEALTHY_NOW;
    }
    if (live) {
        f |= DIAG_FLAG_DATA_LIVE;
    }
    if (persist_ok) {
        f |= DIAG_FLAG_PERSIST_OK;
    }
    return f;
}

/* --- main ---------------------------------------------------------------- */

int main(void)
{
    persist_record_t rec;
    uint8_t  buf[TXFRAME_DLC];
    uint32_t now;
    uint32_t last_slot;
    uint8_t  slot = 0u;
    uint16_t vdd_c;
    uint16_t uptime_s = 0u;
    uint8_t  phase = 0u;
    bool     can_ok;
    bool     persist_ok;
    bool     unhealthy = false;
    /* How many more fast slots LED_CAN should go on reporting a fault. See
     * DIAG_UNHEALTHY_HOLD in config.h. */
    uint8_t  unhealthy_hold = 0u;

    hal_sys_init();

    decode_init(&st);
    compute_init(&cp);

    /* A virgin EEPROM returns false and a zeroed record. That is the correct
     * state for a device that has never run, not an error -- there is nothing
     * to report and nothing to retry. */
    persist_ok = persist_load(&ps, &hal_eeprom_backend, &rec);
    if (persist_ok) {
        compute_restore(&cp, rec.total_ul, rec.total_mm,
                        rec.tank_stable_l, rec.tank_stable_valid);
    }

    /* CAN_START_MODE is HAL_CAN_MODE_NORMAL unless the build said otherwise;
     * see config.h. A silent build still receives, still decodes and still
     * computes -- the only thing it does not do is put anything on the wire. */
    can_ok = hal_can_init(CAN_START_MODE);

    vdd_c = hal_sys_vdd_c();

    now = hal_sys_millis();
    last_slot = now;

    for (;;) {
        hal_sys_watchdog_clear();

        /* Read the clock exactly once per pass and hand that one value to
         * every core call below. Reading it again halfway through can straddle
         * a millisecond and hand compute_tick() a delta of zero where it
         * expects one. */
        now = hal_sys_millis();

        /* Drain the receive FIFO to empty, every pass -- not on a 10 ms slot.
         * RX_POLL_MS in config.h is the guarantee we must not fall behind;
         * draining every pass is far inside it and costs nothing, and it is
         * what keeps the eight-deep FIFO from ever being the binding
         * constraint. */
        if (can_ok) {
            hal_can_frame_t frame;

            while (hal_can_receive(&frame)) {
                if (decode_frame(&st, frame.id, frame.data, frame.dlc)) {
                    /* 0x480 is the heartbeat of the whole device: it carries
                     * the fuel counter and it is the only frame that moves an
                     * accumulator. */
                    if (frame.id == CAN_ID_FUEL) {
                        compute_on_fuel(&cp, &st, now);
                    }
                }
            }
        }

        /* The FIFO is empty now, so this is the one moment an overflow the
         * EEPROM write caused can be cleared without the next frame setting it
         * straight back. */
        if (pardon_overflow) {
            (void)hal_can_overflow();
            pardon_overflow = false;
        }

        /* Integrates distance and samples the tank once a second. Safe to call
         * as often as we like, and it is called on every pass so that neither
         * step depends on a scheduler slot -- but the distance step itself is
         * DIST_TICK_MS, decided inside compute_tick() rather than here.
         * config.h says why, and it is not a cycle count: a one-millisecond
         * step truncates several per cent of the trip away. */
        compute_tick(&cp, &st, now);

        /* ONE SLOT, AT MOST ONE FRAME. config.h carries the measurement this
         * comes from: a receiver with two buffers loses whichever of our
         * frames lands third on the wire, so no two of them may leave inside
         * one pass. Every branch below sends nothing or sends one thing.
         *
         * The slot is missed rather than caught up -- last_slot takes the
         * clock rather than advancing by TX_SLOT_MS -- because catching up
         * after the EEPROM write would fire two slots back to back and
         * rebuild the burst this whole arrangement exists to prevent. */
        if ((uint32_t)(now - last_slot) >= (uint32_t)TX_SLOT_MS) {
            last_slot = now;

            if ((slot & 0x03u) == 0u) {
                phase++;

                vdd_c = hal_sys_vdd_c();

                /* One gather feeds all four frames. 0x601 goes out one slot
                 * later and 0x602 two, so the oldest thing on the wire is
                 * 75 ms behind this -- made of accumulators that move in
                 * seconds. */
                txframes_gather(&tx, &cp, &st, vdd_c, now);

                txframes_fuel(&tx, buf);
                if (!hal_can_send(CAN_ID_TX_FUEL, buf, TXFRAME_DLC)) {
                    tx_fail_count();
                }

                /* Both halves of the same reading, and config.h says why there
                 * are two. An overflow is an instant rather than a state --
                 * hal_can_overflow() clears it as it reports it -- so it is
                 * stretched by the hold below into something a person can
                 * actually see on an LED. */
                if (hal_can_overflow() ||
                    hal_can_rx_errors() != 0u || hal_can_tx_errors() != 0u) {
                    unhealthy = true;
                    unhealthy_hold = DIAG_UNHEALTHY_HOLD;
                } else if (unhealthy_hold > 0u) {
                    unhealthy_hold--;
                }

                leds_update(can_ok, compute_data_live(&cp, now),
                            unhealthy_hold > 0u, phase);
            } else if ((slot & 0x03u) == 1u) {
                txframes_engine(&tx, buf);
                if (!hal_can_send(CAN_ID_TX_ENGINE, buf, TXFRAME_DLC)) {
                    tx_fail_count();
                }
            } else if (slot == (uint8_t)TX_SLOT_TRIP) {
                /* The trip totals are gathered here and not with the rest:
                 * 0x602 goes out once a second, so computing them ten times a
                 * second was two divisions by 1000 for nobody. */
                txframes_gather_trip(&tx, &cp, now);
                txframes_trip(&tx, buf);
                if (!hal_can_send(CAN_ID_TX_TRIP, buf, TXFRAME_DLC)) {
                    tx_fail_count();
                }
            } else if (slot == (uint8_t)TX_SLOT_DIAG) {
                /* This slot comes round once per TX_SLOTS_PER_SEC slots, so
                 * the uptime is a counter here rather than now/1000 -- which
                 * would be a 32-bit division by a constant every second for a
                 * number that advances by exactly one. It saturates: 0xFFFF is
                 * 18 hours and the point of the field is "did this thing reset
                 * behind my back", which a stuck ceiling answers as well as a
                 * wrapping counter answers it badly. */
                if (uptime_s < 0xFFFFu) {
                    uptime_s++;
                }

                /* 0x603 goes out only while the DBG_EN jumper is fitted. In
                 * a closed dashboard nobody is reading it, so a frame a second
                 * and the gather behind it would be bus traffic and CPU spent
                 * on nobody. JP1 already means "somebody is looking at this
                 * device", and this is the second thing it now means --
                 * config.h has the reasoning and docs/frames.md says it where
                 * a reader of the frame layout will find it.
                 *
                 * Note which side of the jumper test the counting sits on:
                 * tx_fail is incremented by the frames above whether or not
                 * anybody is watching, so it is a total since power-up rather
                 * than a total since the jumper went on. */
                if (hal_sys_debug_enabled()) {
                    txframes_gather_diag(&tx,
                                         hal_can_rx_errors(),
                                         hal_can_tx_errors(),
                                         hal_can_status(),
                                         diag_flags(can_ok, unhealthy,
                                                    unhealthy_hold > 0u,
                                                    persist_ok,
                                                    compute_data_live(&cp,
                                                                      now)),
                                         hal_sys_reset_cause(), tx_fail,
                                         uptime_s);
                    txframes_diag(&tx, buf);
                    if (!hal_can_send(CAN_ID_TX_DIAG, buf, TXFRAME_DLC)) {
                        tx_fail_count();
                    }
                }
            } else if (slot == (uint8_t)TX_SLOT_PERSIST) {
                rec.total_ul          = cp.total_ul;
                rec.total_mm          = cp.total_mm;
                rec.tank_stable_l     = cp.tank_stable_l;
                rec.tank_stable_valid = cp.tank_stable_valid;

                /* This slot sends nothing, which is why the EEPROM write is
                 * in it: the write blocks for about 48 ms, and in a slot that
                 * had just transmitted it would push the next frame onto the
                 * heels of the one after.
                 *
                 * persist_save() carries the PERSIST_INTERVAL_MS rule, the
                 * only-on-change rule and the refusal to store an empty record
                 * itself. It is called once a second and allowed to say no; a
                 * second timer here would just be a second thing to get wrong.
                 *
                 * When it does write, it blocks for about 48 ms -- twelve bytes at
                 * the 4 ms typical of DS39977C Table 31-1, D122, three times a
                 * minute since PERSIST_INTERVAL_MS came down -- and the FIFO
                 * will overflow behind it. That is survivable and was checked
                 * rather than assumed:
                 *
                 *   fuel      the counter delta is (new - old) mod 32768, so a gap
                 *             in the frames costs nothing at all; the next 0x480
                 *             accounts for everything burned during the write
                 *   distance  integrated from speed against the clock in
                 *             compute_tick(), not from frame arrivals, and the
                 *             clock keeps running through the write because
                 *             hal_eeprom_write() re-enables interrupts as soon as
                 *             the unlock sequence is over
                 *   tank      sampled once a second from whatever the last frame
                 *             said; 48 ms of staleness is nothing against a float
                 *             that sloshes by nine litres
                 *
                 * The overflow behind it is forgiven so that the LED and
                 * UNHEALTHY go on meaning something -- an overflow we caused on
                 * purpose, three times a minute, is not a fault to report. Not
                 * here, though: the FIFO is still full at this point and the
                 * next frame would set the flag again within a millisecond.
                 * pardon_overflow defers it to just after the next drain, and
                 * the bench found the difference -- at 610 frames a second the
                 * latch fired anyway. */
                if (persist_save(&ps, &rec, now)) {
                    pardon_overflow = true;
                }
            }

            slot++;
            if (slot >= (uint8_t)TX_SLOTS_PER_SEC) {
                slot = 0u;
            }
        }
    }

    /* Not reached. */
}
