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
 *    100 ms       transmit 0x600 and 0x601, sample VDD, update the LEDs
 *    1 s          transmit 0x602, offer the accumulators to the EEPROM
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
 *             2.5 Hz blink  arriving, but the error counters are not zero or
 *                           the FIFO has overflowed
 *             5 Hz blink    hal_can_init() never got the module into the mode
 *                           it asked for; there is no CAN at all
 *             off           the bus has been quiet for DATA_TIMEOUT_MS
 *
 * The distinction that matters on a bench is the last two: dark means the car
 * is not talking, fast blink means we are not listening.
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

static void tx_fail_count(void)
{
    if (tx_fail < 0xFFu) {
        tx_fail++;
    }
}

static uint8_t diag_flags(bool can_ok, bool unhealthy, bool persist_ok,
                          bool live)
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
    uint32_t last_fast;
    uint32_t last_slow;
    uint16_t vdd_c;
    uint16_t uptime_s = 0u;
    uint8_t  phase = 0u;
    bool     can_ok;
    bool     persist_ok;
    bool     unhealthy = false;

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
    last_fast = now;
    last_slow = now;

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

        /* Integrates distance and samples the tank once a second. Safe to call
         * as often as we like, and it is called on every pass so that neither
         * step depends on a scheduler slot -- but the distance step itself is
         * DIST_TICK_MS, decided inside compute_tick() rather than here.
         * config.h says why, and it is not a cycle count: a one-millisecond
         * step truncates several per cent of the trip away. */
        compute_tick(&cp, &st, now);

        if ((uint32_t)(now - last_fast) >= (uint32_t)TX_FAST_MS) {
            last_fast = now;
            phase++;

            vdd_c = hal_sys_vdd_c();

            /* One gather, three frames. 0x602 adds its own two totals in the
             * slow slot below and takes the rest from here, at most 100 ms
             * old and made of accumulators that move in seconds. */
            txframes_gather(&tx, &cp, &st, vdd_c, now);

            txframes_fuel(&tx, buf);
            if (!hal_can_send(CAN_ID_TX_FUEL, buf, TXFRAME_DLC)) {
                tx_fail_count();
            }

            txframes_engine(&tx, buf);
            if (!hal_can_send(CAN_ID_TX_ENGINE, buf, TXFRAME_DLC)) {
                tx_fail_count();
            }

            if (hal_can_overflow() ||
                hal_can_rx_errors() != 0u || hal_can_tx_errors() != 0u) {
                unhealthy = true;
            }

            leds_update(can_ok, compute_data_live(&cp, now), unhealthy, phase);
        }

        if ((uint32_t)(now - last_slow) >= (uint32_t)TX_SLOW_MS) {
            last_slow = now;

            /* The trip totals are gathered here and not in the fast slot:
             * 0x602 goes out once a second, so computing them ten times a
             * second was two divisions by 1000 for nobody. Everything else in
             * tx still comes from the previous fast slot, which is at most
             * 100 ms old and carries accumulators that move in seconds. */
            txframes_gather_trip(&tx, &cp, now);
            txframes_trip(&tx, buf);
            if (!hal_can_send(CAN_ID_TX_TRIP, buf, TXFRAME_DLC)) {
                tx_fail_count();
            }

            /* One slow slot is one second by construction, so the uptime is a
             * counter here rather than now/1000 -- which would be a 32-bit
             * division by a constant every second for a number that advances
             * by exactly one. It saturates: 0xFFFF is 18 hours and the point
             * of the field is "did this thing reset behind my back", which a
             * stuck ceiling answers as well as a wrapping counter answers it
             * badly. */
            if (uptime_s < 0xFFFFu) {
                uptime_s++;
            }

            /* 0x603 goes out only while the DBG_EN jumper is fitted. In a
             * closed dashboard nobody is reading it, so a frame a second and
             * the gather behind it would be bus traffic and CPU spent on
             * nobody. JP1 already means "somebody is looking at this device",
             * and this is the second thing it now means -- config.h has the
             * reasoning and docs/frames.md says it where a reader of the frame
             * layout will find it.
             *
             * Note which side of the jumper test the counting sits on:
             * tx_fail is incremented by the frames above whether or not
             * anybody is watching, so it is a total since power-up rather than
             * a total since the jumper went on. */
            if (hal_sys_debug_enabled()) {
                txframes_gather_diag(&tx,
                                     hal_can_rx_errors(), hal_can_tx_errors(),
                                     hal_can_status(),
                                     diag_flags(can_ok, unhealthy, persist_ok,
                                                compute_data_live(&cp, now)),
                                     hal_sys_reset_cause(), tx_fail, uptime_s);
                txframes_diag(&tx, buf);
                if (!hal_can_send(CAN_ID_TX_DIAG, buf, TXFRAME_DLC)) {
                    tx_fail_count();
                }
            }

            rec.total_ul          = cp.total_ul;
            rec.total_mm          = cp.total_mm;
            rec.tank_stable_l     = cp.tank_stable_l;
            rec.tank_stable_valid = cp.tank_stable_valid;

            /* persist_save() carries the PERSIST_INTERVAL_MS rule, the
             * only-on-change rule and the refusal to store an empty record
             * itself. Call it every second and let it say no; a second timer
             * here would just be a second thing to get wrong.
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
             * The overflow flag is cleared afterwards so that the LED goes on
             * meaning something. An overflow we caused on purpose, once a
             * minute, is not a fault to report. */
            if (persist_save(&ps, &rec, now)) {
                (void)hal_can_overflow();
            }
        }
    }

    /* Not reached. */
}
