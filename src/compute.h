/* compute.h -- the arithmetic. PURE C, no hardware.
 *
 * Everything is scaled integers. The PIC18 has no floating point unit, the
 * accumulators have to be exact, and every quantity we transmit ends up as an
 * integer on the wire anyway -- so a float would only be a place for rounding
 * to hide.
 *
 * Three entry points drive it:
 *
 *   compute_on_fuel()  called for every 0x480, which is the heartbeat of the
 *                      whole device. 0x480 HAS NO FIXED PERIOD -- it arrives
 *                      on a 10 ms grid, 26/s at idle and 18/s at 2600 rpm, so
 *                      nothing here may assume a rate. See can-decoding.md
 *                      question 1.
 *   compute_tick()     called on the scheduler tick: integrates distance and
 *                      samples the tank
 *   compute_on_engine() called for every 0x280: grades the idle and watches
 *                      the start, for the health frame 0x604
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

/* One bucket of the flow window: everything burned in a quarter of a second,
 * and how long that quarter second really was. Both fit a uint16 because a
 * bucket closes at FLOW_BUCKET_MS and compute_on_fuel refuses to add a sample
 * more than FLOW_WINDOW_MS long. */
typedef struct {
    uint16_t ul;                /* fuel burned in this bucket */
    uint16_t ms;                /* over this long             */
} flow_bucket_t;

/* The engine-health state behind 0x604. None of it is persisted and none of
 * it is cleared by a refuelling: it describes the current engine start, and
 * compute_on_engine() clears it itself when the next one begins. Every field
 * mirrors a variable of roughness() or start_fields() in tools/idledips.py,
 * which are its oracles -- replay.py --host-build diffs the two exactly. */
typedef struct {
    /* --- the idle grade ------------------------------------------------- */
    uint32_t rough_acc;         /* quarter-rpm steps << ROUGH_SHIFT          */
    uint32_t base;              /* idle baseline, quarter rpm << IDLE_BASE_SHIFT */
    uint32_t idle_since_ms;     /* the settle delay runs from here           */
    uint32_t prev_ms;           /* previous gated frame, for the idle clock  */
    uint32_t idle_ms;           /* settled idle graded this start            */
    uint16_t prev_rpm_q4;       /* the last VALUE of the field, not frame    */
    bool     in_gate;           /* base and idle_since_ms mean something     */
    bool     have_prev_ms;
    bool     have_prev_rpm;
    bool     idling;            /* settled on the last frame                 */

    /* --- the start ------------------------------------------------------ */
    uint8_t  start_phase;       /* HEALTH_START_* in compute.c               */
    bool     start_seen;        /* the current start was watched from rest   */
    uint32_t start_ms;          /* first turn, then first firing             */
    uint16_t fire_rpm;
    uint16_t low_rpm;
    uint8_t  start_crank;       /* the three fields as they go on the wire,  */
    uint8_t  start_dip;         /* HEALTH_UNKNOWN until measured             */
    uint8_t  start_clt;
} health_t;

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
    flow_bucket_t flow[FLOW_BUCKETS];
    uint8_t  flow_open;         /* the bucket still being filled            */
    uint32_t flow_ul_s;         /* the answer, microlitres per second       */

    /* --- distance ------------------------------------------------------- */
    uint32_t last_tick_ms;
    /* What the last division by 3600 left over, carried into the next step so
     * the integration has no bias at all. Always under 3600, i.e. under one
     * millimetre of distance. See DIST_TICK_MS in config.h. */
    uint16_t dist_rem;
    bool     have_tick;

    /* --- the rolling basis behind Range, updated once per kilometre ------ */
    uint32_t seg_cur_ul;        /* burned so far in the kilometre in progress */
    uint32_t seg_cur_mm;        /* and how far into it we are                 */
    /* Consumption in 0.1 l/100 km shifted up by RANGE_BASIS_Q4, so the filter
     * can move in steps smaller than a display digit. IT IS NEVER ZERO --
     * compute_init() opens it at the default, compute_restore() seeds it from
     * the persisted trip average and compute_reset_trip() leaves it alone.
     * config.h says what it cost when it could be. */
    uint16_t basis_q4;

    /* --- tank level, the settled baseline and the refuelling trigger ----- */
    /* The settled at-rest level in 1/256 litre, so the filter needs no
     * division: a uint16 holds 127 l comfortably. tank_stable_l is its whole
     * part and the only piece that reaches the EEPROM. */
    uint16_t tank_rest_q8;
    uint8_t  refuel_high;       /* consecutive at-rest samples above the rise */
    uint8_t  rest_s;            /* consecutive at-rest samples, saturating at
                                 * REFUEL_ARM_S. Below it the refuelling rule
                                 * is not armed: the float is still settling
                                 * from whatever the car was just doing.      */
    bool     have_moved;        /* the car has been seen moving since the
                                 * ignition came on. It separates ARRIVING at
                                 * a stop, where the reference may take up the
                                 * level found there, from STARTING at one,
                                 * where the EEPROM reference is the only
                                 * truth there is. config.h says why.         */
    uint8_t  tank_stable_l;     /* settled level at rest; survives in EEPROM */
    bool     tank_stable_valid;
    uint32_t tank_damped_ml;    /* 0.001 l, first order, TANK_DAMP_SAMPLES  */
    bool     tank_damped_valid;
    uint32_t last_tank_ms;
    uint32_t refuels;           /* how often the trip was cleared           */

    /* --- liveness ------------------------------------------------------- */
    uint32_t last_data_ms;
    bool     have_data;

    /* --- engine health, for 0x604 --------------------------------------- */
    health_t health;
} compute_t;

/* Empty accumulators, nothing known yet. */
void compute_init(compute_t *c);

/* Clear only what the average is made of. The tank state, the flow window and
 * the rolling Range basis survive -- they describe the present, not the trip,
 * and a tankful of fuel does not change how the car is being driven. */
void compute_reset_trip(compute_t *c);

/* Restore what persist.c read back out of the EEPROM. Called once at start-up
 * and never again, AFTER compute_init(), whose defaults it overwrites where
 * the record has something better. It seeds both filters -- the tank baseline
 * and the Range basis -- rather than leaving either to be established by the
 * first sample or the first kilometre after the key turn. */
void compute_restore(compute_t *c, uint32_t total_ul, uint32_t total_mm,
                     uint8_t tank_stable_l, bool tank_stable_valid);

/* One 0x480 frame. This is where the counter delta, the restart rule and the
 * flow window live. now_ms is a free-running millisecond clock. */
void compute_on_fuel(compute_t *c, const decode_state_t *st, uint32_t now_ms);

/* Scheduler tick: integrates distance since the previous tick and samples the
 * tank once a second. Safe to call as often as you like. */
void compute_tick(compute_t *c, const decode_state_t *st, uint32_t now_ms);

/* One 0x280 frame, already folded into st. Steps the idle grade on a change of
 * the engine-speed field and runs the start detector; see config.h, 0x604.
 * now_ms is the same free-running clock the other two take. No loop, no
 * division and no multiplication beyond a shift -- it runs 94 times a second. */
void compute_on_engine(compute_t *c, const decode_state_t *st, uint32_t now_ms);

/* The health frame's bytes, in wire units, HEALTH_UNKNOWN where not known.
 * Called once a second from the health slot, so the one division by 1000 in
 * the idle seconds costs nothing that matters. */
uint8_t compute_idle_rough(const compute_t *c);     /* 1/32 rpm            */
uint8_t compute_idle_health(const compute_t *c);    /* 0-200, 100 = before */
uint8_t compute_idle_s(const compute_t *c);         /* seconds, saturating */

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
/* Range from the damped tank level, never the instantaneous one -- see the
 * comment on the definition. Takes no decode_state_t for that reason. */
uint16_t compute_range_km(const compute_t *c);

/* Trip totals for the slow diagnostic frame. */
uint32_t compute_trip_ml(const compute_t *c);       /* 0.001 l             */
uint32_t compute_trip_m(const compute_t *c);        /* metres              */

/* These two only need the bus state, so they carry no accumulator.
 *
 * Power takes the torque the caller has already computed rather than computing
 * it again. It is the same number both times, and txframes_gather transmits
 * both, so working it out twice cost 1,042 cycles -- 11 % of the slot the
 * gather runs in --
 * for nothing. Passing zero is not a way to disable it: the gates live in
 * compute_torque_d(), and a zero torque is exactly what makes power zero. */
uint16_t compute_torque_d(const decode_state_t *st);  /* 0.1 Nm, net       */

/* Apply TORQUE_TRIM_PCT, carried as 1/256, to a scaled value. Public only so
 * that a test can drive it with trims this build was not compiled with: the
 * constant is a compile-time one, so a test that could only see the default
 * would be no test of the arithmetic at all. Saturates at zero rather than
 * wrapping, which only a trim past -100 % could ask for and the range check in
 * config.h already refuses. */
uint32_t compute_trim_apply(uint32_t value, int16_t trim_q8);
uint16_t compute_power_d(const decode_state_t *st,
                         uint16_t torque_d);          /* 0.1 kW            */

#endif /* COMPUTE_H */
