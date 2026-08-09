/* compute.h -- the arithmetic. PURE C, no hardware.
 *
 * Everything is scaled integers. The PIC18 has no floating point unit, the
 * accumulators have to be exact, and every quantity we transmit ends up as an
 * integer on the wire anyway -- so a float would only be a place for rounding
 * to hide.
 *
 * Two entry points drive it:
 *
 *   compute_on_fuel()  called for every 0x480, which is the heartbeat of the
 *                      whole device at 49.5 ms
 *   compute_tick()     called on the scheduler tick: integrates distance and
 *                      samples the tank
 *
 * Everything else is a getter that converts the accumulators into the unit a
 * frame wants. They are cheap and stateless, so main.c can call them straight
 * from the transmit slot.
 */
#ifndef COMPUTE_H
#define COMPUTE_H

#include <stdbool.h>
#include <stdint.h>

#include "config.h"
#include "decode.h"

typedef struct {
    uint16_t ul;                /* fuel burned in this sample */
    uint16_t ms;                /* how long it took           */
} flow_sample_t;

typedef struct {
    /* --- the trip accumulators, cleared on refuelling and persisted ----- */
    uint32_t total_ul;          /* microlitres since the last reset         */
    uint32_t total_mm;          /* millimetres since the last reset         */

    /* --- fuel counter tracking ----------------------------------------- */
    uint16_t prev_counter;
    bool     have_prev;
    uint32_t last_fuel_ms;
    uint32_t restarts;          /* how often the engine-off rule fired      */

    /* --- sliding window the instantaneous flow is averaged over --------- */
    flow_sample_t flow[FLOW_WINDOW_SLOTS];
    uint8_t  flow_head;         /* index of the oldest sample               */
    uint8_t  flow_count;
    uint32_t flow_sum_ul;
    uint32_t flow_sum_ms;
    uint32_t flow_ul_s;         /* the answer, microlitres per second       */

    /* --- distance ------------------------------------------------------- */
    uint32_t last_tick_ms;
    bool     have_tick;

    /* --- rolling window behind Range, one slot per kilometre ------------ */
    uint32_t seg_ul[RANGE_SEGMENTS];
    uint8_t  seg_next;
    uint8_t  seg_count;
    uint32_t seg_cur_ul;
    uint32_t seg_cur_mm;

    /* --- tank level, its median and the refuelling trigger -------------- */
    uint8_t  tank_hist[TANK_MEDIAN_SLOTS];
    uint8_t  tank_hist_count;
    uint8_t  tank_hist_next;
    uint8_t  tank_stable_l;     /* median at rest; survives in EEPROM       */
    bool     tank_stable_valid;
    uint32_t tank_damped_ml;    /* 0.001 l, first order over 60 s           */
    bool     tank_damped_valid;
    uint32_t last_tank_ms;
    bool     have_tank_ms;
    uint32_t refuels;           /* how often the trip was cleared           */

    /* --- liveness ------------------------------------------------------- */
    uint32_t last_data_ms;
    bool     have_data;
} compute_t;

/* Empty accumulators, nothing known yet. */
void compute_init(compute_t *c);

/* Clear only what the average is made of. The tank state and the flow window
 * survive -- they describe the present, not the trip. */
void compute_reset_trip(compute_t *c);

/* Restore what persist.c read back out of the EEPROM. Called once at start-up
 * and never again; it does not touch the derived state. */
void compute_restore(compute_t *c, uint32_t total_ul, uint32_t total_mm,
                     uint8_t tank_stable_l, bool tank_stable_valid);

/* One 0x480 frame. This is where the counter delta, the restart rule and the
 * flow window live. now_ms is a free-running millisecond clock. */
void compute_on_fuel(compute_t *c, const decode_state_t *st, uint32_t now_ms);

/* Scheduler tick: integrates distance since the previous tick and samples the
 * tank once a second. Safe to call as often as you like. */
void compute_tick(compute_t *c, const decode_state_t *st, uint32_t now_ms);

/* False once the bus has gone quiet for longer than DATA_TIMEOUT_MS. The
 * transmitted frames then go to zero rather than freezing at their last
 * reading, which would look plausible and be wrong. */
bool compute_data_live(const compute_t *c, uint32_t now_ms);

/* --- derived quantities, in the units the frames use --------------------- */

uint16_t compute_flow_lh_c(const compute_t *c);     /* 0.01 l/h            */
uint16_t compute_fuel_now_d(const compute_t *c,
                            const decode_state_t *st); /* 0.1, dual unit   */
uint16_t compute_avg_l100_d(const compute_t *c);    /* 0.1 l/100 km        */
uint16_t compute_tank_d(const compute_t *c);        /* 0.1 l, damped       */
uint16_t compute_range_km(const compute_t *c, const decode_state_t *st);

/* Trip totals for the slow diagnostic frame. */
uint32_t compute_trip_ml(const compute_t *c);       /* 0.001 l             */
uint32_t compute_trip_m(const compute_t *c);        /* metres              */

/* These two only need the bus state, so they carry no accumulator. */
uint16_t compute_torque_d(const decode_state_t *st);  /* 0.1 Nm, net       */
uint16_t compute_power_d(const decode_state_t *st);   /* 0.1 kW            */

#endif /* COMPUTE_H */
