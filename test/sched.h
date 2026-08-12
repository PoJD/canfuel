/* sched.h -- replay a fixture through the core THE WAY main.c DRIVES IT.
 *
 * Header only, like the rest of test/.
 *
 * WHY THIS EXISTS, AND IT IS NOT A SECOND replay_core.h. replay_core.h feeds
 * the core off the 0x480 frames: one call to compute_tick() per fuel frame,
 * about 38 ms apart. That is how tools/replay.py works and it is the right
 * shape for diffing the two implementations against each other.
 *
 * It is NOT how the firmware runs. main.c calls compute_tick() on every pass
 * of the scheduler, which on the real part is every ~100 us, and drains the
 * CAN FIFO on every pass as well. Everything that depends on HOW OFTEN the
 * core is called is therefore invisible to replay_core.h -- and on 2026-08-12
 * exactly that hid a 6.4 % under-reading of every distance the device would
 * have reported, because v * 1 ms / 3600 truncates to whole millimetres.
 * The fixtures agreed with Python about a wrong number for weeks.
 *
 * So this harness runs a millisecond clock and reproduces main.c's structure:
 *
 *   every tick_ms      deliver whatever frames have arrived, compute_tick()
 *   every TX_FAST_MS   txframes_gather() -- the getters, at their real rate
 *   every TX_SLOW_MS   txframes_gather_trip(), and the once-a-minute EEPROM
 *                      write simulated as a blocking gap that loses frames
 *
 * The tick is a parameter on purpose: the property that matters is that the
 * answers do not depend on it. test_scheduler.c is where that is asserted.
 */
#ifndef SCHED_H
#define SCHED_H

#include <string.h>

#include "compute.h"
#include "config.h"
#include "decode.h"
#include "logread.h"
#include "txframes.h"

/* The EEPROM write blocks for twelve bytes at the 4 ms typical of DS39977C
 * Table 31-1, D122. main.c's comment argues that the frames lost behind it
 * cost nothing; sched_eeprom_blindness_costs_nothing() is where that argument
 * is finally tested rather than asserted. */
#define SCHED_EEPROM_BLOCK_MS   48u

typedef struct {
    uint32_t tick_ms;           /* how often main.c is imagined to come round */
    uint32_t jitter_ms;         /* ... plus 0..jitter, because it is not a timer */
    bool     eeprom_writes;     /* simulate the blocking write and its losses */
} sched_opts_t;

/* The real loop is not a timer. A pass takes 50-130 us depending on how many
 * frames were waiting, and every hundredth one carries the whole transmit slot
 * -- so the interval between two calls to compute_tick() is irregular by a
 * factor of thirty. A fixed tick is the easy case; jitter is the honest one,
 * and anything that only works on a regular grid fails here. */
static inline uint32_t sched_jitter(uint32_t *seed, uint32_t span)
{
    uint32_t x = *seed;
    x ^= x << 13; x ^= x >> 17; x ^= x << 5;
    *seed = x;
    return span == 0u ? 0u : x % (span + 1u);
}

typedef struct {
    decode_state_t st;
    compute_t      cp;
    tx_values_t    tx;          /* the last gather, i.e. what 0x600/0x601 held */
    uint32_t       span_ms;
    size_t         frames_seen;
    size_t         frames_lost; /* dropped behind an EEPROM write */
    size_t         gathers;
    /* The extremes over EVERY gather, not just the last one. A test that says
     * it checked three thousand frames and checked the one left in the struct
     * at the end is worse than no test: it reads as coverage and is not. */
    uint16_t       max_fuel_now_d;
    uint16_t       max_fuel_avg_d;
    uint16_t       max_range_km;
    uint32_t       counter_sum_ul;  /* every delta, added up independently */
} sched_result_t;

/* The independent fuel total. compute_on_fuel() has the restart rule inside
 * it, so this repeats the rule rather than the arithmetic: what it checks is
 * that total_ul is the sum of exactly the deltas the rule accepts. */
static inline void sched_shadow_counter(sched_result_t *r, uint16_t counter,
                                        uint16_t rpm_q4, bool *have,
                                        uint16_t *prev)
{
    if (counter == 0u || rpm_q4 == 0u) {
        *prev = counter;
        *have = true;
        return;
    }
    if (!*have) {
        *prev = counter;
        *have = true;
        return;
    }
    r->counter_sum_ul += (uint16_t)((counter - *prev) % COUNTER_MODULO);
    *prev = counter;
}

/* Only fixtures that carry real timestamps can be run here: a synthetic clock
 * derived from the frames themselves would defeat the whole point, which is to
 * decouple the clock from the arrivals. Returns false for the others. */
static inline bool sched_run(const char *name, sched_opts_t o,
                             sched_result_t *r)
{
    log_file_t lf;
    size_t next = 0;
    uint32_t now, first, last;
    uint32_t last_fast, last_slow, last_write;
    uint32_t blocked_until = 0;
    uint32_t jseed = 0x2545F491u;
    bool     shadow_have = false;
    uint16_t shadow_prev = 0;

    if (!log_load(name, &lf, true)) {
        return false;
    }
    if (!lf.timestamped || lf.count == 0) {
        log_free(&lf);
        return false;
    }

    memset(r, 0, sizeof *r);
    decode_init(&r->st);
    compute_init(&r->cp);

    first = (uint32_t)lf.frames[0].ts_ms;
    last  = (uint32_t)lf.frames[lf.count - 1].ts_ms;
    now = first;
    last_fast = now;
    last_slow = now;
    last_write = now;

    for (;;) {
        /* Deliver every frame that has arrived since the previous pass. The
         * module fills its FIFO whether or not the CPU is listening, so a
         * frame that arrives while the EEPROM write blocks is lost rather
         * than delayed -- that is the part worth simulating. */
        while (next < lf.count && (uint32_t)lf.frames[next].ts_ms <= now) {
            const log_frame_t *f = &lf.frames[next++];

            if (blocked_until != 0u && (uint32_t)f->ts_ms < blocked_until) {
                r->frames_lost++;
                continue;
            }
            r->frames_seen++;
            if (!decode_frame(&r->st, f->can_id, f->data, f->dlc)) {
                continue;
            }
            if (f->can_id == CAN_ID_FUEL) {
                sched_shadow_counter(r, r->st.fuel_counter, r->st.rpm_q4,
                                     &shadow_have, &shadow_prev);
                compute_on_fuel(&r->cp, &r->st, now);
            }
        }

        compute_tick(&r->cp, &r->st, now);

        if ((uint32_t)(now - last_fast) >= (uint32_t)TX_FAST_MS) {
            last_fast = now;
            txframes_gather(&r->tx, &r->cp, &r->st, 503, now);
            r->gathers++;
            if (r->tx.fuel_now_d > r->max_fuel_now_d) {
                r->max_fuel_now_d = r->tx.fuel_now_d;
            }
            if (r->tx.fuel_avg_d > r->max_fuel_avg_d) {
                r->max_fuel_avg_d = r->tx.fuel_avg_d;
            }
            if (r->tx.range_km > r->max_range_km) {
                r->max_range_km = r->tx.range_km;
            }
        }

        if ((uint32_t)(now - last_slow) >= (uint32_t)TX_SLOW_MS) {
            last_slow = now;
            txframes_gather_trip(&r->tx, &r->cp, now);

            /* persist_save() decides for itself once a minute. Here only its
             * cost is modelled: the clock keeps running through the write --
             * hal_eeprom_write() restores GIE as soon as the unlock sequence
             * is over -- but nothing is received.
             *
             * NO WRITE IN THE LAST SECOND OF THE RECORDING, and the reason is
             * the property itself rather than convenience. "A gap costs
             * nothing" is exactly the statement "the next 0x480 after the gap
             * accounts for everything burned during it", because the counter
             * is absolute. A gap with no next frame is outside that claim: the
             * fuel really is unaccounted, and in a car it never happens
             * because the engine does not stop at the same instant the write
             * does. Without this guard the harness manufactures that case at
             * the end of every log and the test measures the fixture's
             * length rather than the firmware. */
            if (o.eeprom_writes &&
                (uint32_t)(last - now) > (uint32_t)SCHED_EEPROM_BLOCK_MS + 1000u &&
                (uint32_t)(now - last_write) >= (uint32_t)PERSIST_INTERVAL_MS) {
                last_write = now;
                blocked_until = now + SCHED_EEPROM_BLOCK_MS;
                now = blocked_until;
            }
        }

        if (now >= last && next >= lf.count) {
            break;
        }
        now += o.tick_ms + sched_jitter(&jseed, o.jitter_ms);
    }

    r->span_ms = last - first;
    log_free(&lf);
    return true;
}

#endif /* SCHED_H */
