/* replay_core.h -- run a whole fixture through decode.c and compute.c.
 *
 * The exact counterpart of the loop in tools/replay.py, so that the numbers
 * the two produce can be compared. Header only; shared by test_compute.c,
 * test_txframes.c and replay_host.c.
 *
 * The frame 0x480 is the clock of the device: it is the only periodic input
 * whose period we trust (49.5 ms, argued in docs/can-decoding.md). Logs in
 * the viewer format carry real timestamps and those are used instead.
 */
#ifndef REPLAY_CORE_H
#define REPLAY_CORE_H

#include "compute.h"
#include "decode.h"
#include "logread.h"

typedef struct {
    decode_state_t st;
    compute_t      cp;
    uint32_t       span_ms;     /* first to last 0x480 */
    size_t         frames;
    size_t         fuel_frames;
    bool           timestamped;
} replay_result_t;

/* Synthetic clock for the five oldest fixtures, which carry no timestamps at
 * all: n * 49.5 ms, rounded to whole milliseconds because that is the
 * resolution the firmware's timer has.
 *
 * THE PERIOD IS FICTIONAL AND IS KNOWN TO BE. 0x480 has no fixed period --
 * measured with adapter timestamps it is 26.4 frames/s at idle and 18.0 at
 * 2586 rpm (can-decoding.md question 1). This exists so the two
 * implementations can be diffed against each other on those five logs, which
 * needs *a* clock rather than a correct one; every duration, flow and distance
 * derived from them is invalid as a fact about the car. The fuel totals are
 * not, because the counter is absolute. Use a _z1 fixture for anything that
 * has to be true. */
static inline uint32_t replay_synthetic_ms(uint32_t n)
{
    return (n * 99u + 1u) / 2u;
}

static inline bool replay_log(const char *name, replay_result_t *r)
{
    log_file_t lf;
    size_t i;
    uint32_t n480 = 0;
    uint32_t first_ms = 0, last_ms = 0;

    if (!log_load(name, &lf, true)) {
        return false;
    }

    decode_init(&r->st);
    compute_init(&r->cp);
    r->frames = lf.count;
    r->fuel_frames = 0;
    r->timestamped = lf.timestamped;

    for (i = 0; i < lf.count; i++) {
        const log_frame_t *f = &lf.frames[i];
        uint32_t now_ms;

        decode_frame(&r->st, f->can_id, f->data, f->dlc);

        if (f->can_id != CAN_ID_FUEL) {
            continue;
        }
        now_ms = r->timestamped ? (uint32_t)f->ts_ms : replay_synthetic_ms(n480);
        if (n480 == 0) {
            first_ms = now_ms;
        }
        last_ms = now_ms;
        n480++;

        /* Distance first, then the counter -- the same order as replay.py. */
        compute_tick(&r->cp, &r->st, now_ms);
        compute_on_fuel(&r->cp, &r->st, now_ms);
    }

    r->fuel_frames = n480;
    r->span_ms = last_ms - first_ms;
    log_free(&lf);
    return true;
}

#endif /* REPLAY_CORE_H */
