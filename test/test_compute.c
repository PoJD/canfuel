/* test_compute.c -- the C twin of the Compute tests in tools/test_replay.py.
 * Same fixtures, same expected numbers.
 *
 * Where Python works in floats and this works in scaled integers, the
 * tolerance is stated and is always smaller than one step of the value that
 * ends up on the display.
 */

#include "compute.h"
#include "config.h"
#include "decode.h"
#include "replay_core.h"
#include "tt.h"

/* A bus state that says: engine running, counter reads this. */
static decode_state_t running(uint16_t counter, uint16_t rpm)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = (uint16_t)(rpm * 4u);
    st.fuel_counter = counter;
    st.fuel_counter_valid = true;
    return st;
}

/* --- trap 2: the counter resets when the ignition goes off -------------- */

static void test_normal_delta(void)
{
    compute_t c;
    decode_state_t a = running(1000, 800), b = running(1050, 800);
    compute_init(&c);
    compute_on_fuel(&c, &a, 0);
    compute_on_fuel(&c, &b, 50);
    TT_EQ(c.total_ul, 50);
    TT_EQ(c.restarts, 0);
}

static void test_wrap_at_32768(void)
{
    compute_t c;
    decode_state_t a = running(32700, 800), b = running(9, 800);
    compute_init(&c);
    compute_on_fuel(&c, &a, 0);
    compute_on_fuel(&c, &b, 50);
    TT_EQ(c.total_ul, 77);
}

static void test_ignition_off_does_not_produce_a_jump(void)
{
    compute_t c;
    decode_state_t a = running(12000, 800), b = running(12100, 800);
    decode_state_t off = running(0, 0), back = running(30, 800);
    compute_init(&c);
    compute_on_fuel(&c, &a, 0);
    compute_on_fuel(&c, &b, 50);
    TT_EQ(c.total_ul, 100);

    compute_on_fuel(&c, &off, 99);      /* ignition off */
    compute_on_fuel(&c, &back, 149);    /* and back on  */

    /* Only the 30 ul actually burned after the restart is counted. Without
     * detection the delta would be (0 - 12100) mod 32768 = 20,668. */
    TT_EQ(c.total_ul, 130);
    TT_EQ(c.restarts, 1);
}

static void test_engine_stopped_resets_reference(void)
{
    compute_t c;
    decode_state_t a = running(5000, 800), stopped = running(5000, 0);
    decode_state_t b = running(5100, 800);
    compute_init(&c);
    compute_on_fuel(&c, &a, 0);
    compute_on_fuel(&c, &stopped, 50);
    compute_on_fuel(&c, &b, 100);
    TT_EQ(c.total_ul, 100);
}

static void test_engine_stopped_zeroes_the_flow(void)
{
    compute_t c;
    decode_state_t a = running(1000, 800), b = running(1050, 800);
    decode_state_t stopped = running(1050, 0);
    compute_init(&c);
    compute_on_fuel(&c, &a, 0);
    compute_on_fuel(&c, &b, 50);
    TT_TRUE(c.flow_ul_s > 0);
    compute_on_fuel(&c, &stopped, 100);
    /* Freezing at the last flow would show a plausible, wrong number on a
     * parked car. */
    TT_EQ(c.flow_ul_s, 0);
}

/* --- FuelNow, the dual unit --------------------------------------------- */

static uint16_t fuel_now(uint32_t speed_mmh, uint32_t flow_ul_s, bool valid)
{
    compute_t c;
    decode_state_t st;
    compute_init(&c);
    decode_init(&st);
    st.speed_mmh = speed_mmh;
    st.speed_valid = valid;
    c.flow_ul_s = flow_ul_s;
    return compute_fuel_now_d(&c, &st);
}

static void test_below_threshold_is_litres_per_hour(void)
{
    /* 310 ul/s is the measured idle flow: 1.116 l/h, so 1.1 on the display. */
    TT_EQ(fuel_now(3900, 310, true), 11);
}

static void test_at_threshold_switches_unit(void)
{
    /* 310 ul/s at exactly 4.000 km/h is 27.9 l/100 km, not 1.1 l/h. */
    TT_EQ(fuel_now(4000, 310, true), 279);
}

static void test_no_hysteresis(void)
{
    /* A single threshold. The jump is deliberate -- it is the cue that the
     * unit switched. */
    TT_EQ(fuel_now(3999, 500, true), 18);       /* 1.8 l/h      */
    TT_EQ(fuel_now(4000, 500, true), 450);      /* 45.0 l/100km */
}

static void test_clamped_to_999(void)
{
    TT_EQ(fuel_now(4000, 100000, true), FUELNOW_CLAMP_D);
    TT_EQ(fuel_now(0, 10000000, true), FUELNOW_CLAMP_D);
}

static void test_invalid_speed_falls_back_to_flow(void)
{
    /* 50 km/h but the gate says the reading is not trustworthy. */
    TT_EQ(fuel_now(50000, 310, false), 11);     /* l/h, not l/100 km */
}

static void test_zero_flow(void)
{
    TT_EQ(fuel_now(0, 0, true), 0);
    TT_EQ(fuel_now(50000, 0, true), 0);
}

static void test_documented_table(void)
{
    /* The table from docs/frames.md, FuelNow. Flow is given
     * in l/h there, so it is converted to ul/s first: l/h * 1000 / 3.6. */
    struct { uint32_t kmh; uint32_t flow_lh_c; uint16_t expect; } cases[] = {
        {  4, 150, 375 }, {  6, 150, 250 }, { 10, 150, 150 },
        {  6, 300, 500 }, { 20, 300, 150 }, { 10, 600, 600 },
        {  4, 600, FUELNOW_CLAMP_D },       /* 150 l/100 km, clamped */
    };
    size_t i;
    for (i = 0; i < sizeof cases / sizeof cases[0]; i++) {
        uint32_t ul_s = (cases[i].flow_lh_c * 10000u + 1800u) / 3600u;
        TT_NEAR(fuel_now(cases[i].kmh * 1000u, ul_s, true), cases[i].expect, 1);
    }
}

/* --- FuelAvg ------------------------------------------------------------ */

static void test_average_below_minimum_distance_is_zero(void)
{
    /* Dividing by an almost-zero distance gave 21,395 l/100 km on
     * 06_trip_reset before the car had moved. */
    compute_t c;
    compute_init(&c);
    c.total_ul = 17544;
    c.total_mm = AVG_MIN_MM - 1u;
    TT_EQ(compute_avg_l100_d(&c), 0);
}

static void test_average_is_a_ratio_of_accumulators(void)
{
    compute_t c;
    compute_init(&c);
    c.total_ul = 700000;        /* 0.7 l  */
    c.total_mm = 10000000;      /* 10 km  */
    TT_EQ(compute_avg_l100_d(&c), 70);      /* 7.0 l/100 km */
}

static void test_idling_does_not_ruin_the_average(void)
{
    compute_t c;
    uint16_t before;
    compute_init(&c);
    c.total_ul = 700000;
    c.total_mm = 10000000;
    before = compute_avg_l100_d(&c);
    c.total_ul += 18652;        /* one minute of idling, measured */
    TT_TRUE(compute_avg_l100_d(&c) - before < 30);
}

/* --- distance integration ------------------------------------------------ *
 *
 * THE FAULT THESE EXIST FOR, because no fixture could ever show it. main.c
 * calls compute_tick() on every pass of the scheduler and a pass is about
 * 113 us on the real part, so the delta it sees in the car is ONE
 * MILLISECOND -- while replay_core.h ticks on the 0x480 frames, ~38 ms apart.
 * v * 1 ms / 3600 truncated to whole millimetres throws away 0.89 mm of every
 * 13.89 at 50 km/h (6.4 % of the trip, the average and the range) and
 * everything at all below 3.6 km/h.
 *
 * So the property under test is that the answer does not depend on how often
 * the core is asked -- which is what DIST_TICK_MS and the carried remainder
 * are for. */

static void distance_ticks(compute_t *c, decode_state_t *st, uint32_t *now,
                           uint32_t step_ms, uint32_t total_ms)
{
    uint32_t t;
    for (t = 0; t < total_ms; t += step_ms) {
        *now += step_ms;
        compute_tick(c, st, *now);
    }
}

static void test_distance_does_not_depend_on_the_tick_rate(void)
{
    compute_t fast, slow;
    decode_state_t st;
    uint32_t now_f = 0, now_s = 0;

    decode_init(&st);
    st.speed_valid = true;
    st.speed_mmh = 50000u;                  /* 50 km/h = 13.889 mm/ms */

    compute_init(&fast);
    compute_tick(&fast, &st, 0);            /* the first call only starts it */
    distance_ticks(&fast, &st, &now_f, 1u, 10000u);

    compute_init(&slow);
    compute_tick(&slow, &st, 0);
    distance_ticks(&slow, &st, &now_s, 1000u, 10000u);

    /* Ten seconds at 50 km/h is 138,888.9 mm. The millisecond loop used to
     * report 130,000 of it. */
    TT_NEAR(fast.total_mm, 138888u, 20u);
    TT_NEAR(slow.total_mm, 138888u, 20u);
}

static void test_walking_pace_still_covers_ground(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;

    compute_init(&c);
    decode_init(&st);
    st.speed_valid = true;
    st.speed_mmh = 3000u;                   /* 3 km/h, a car park */

    compute_tick(&c, &st, 0);
    distance_ticks(&c, &st, &now, 1u, 60000u);

    /* Under 3.6 km/h the old one-millisecond quotient was zero every single
     * time, so a minute of manoeuvring covered nothing whatsoever. It is
     * 50 m. */
    TT_NEAR(c.total_mm, 50000u, 20u);
}

static void test_a_standing_car_covers_no_distance(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;

    compute_init(&c);
    decode_init(&st);
    st.speed_valid = true;
    st.speed_mmh = 5u;                      /* raw 1 -- what standing sends */

    compute_tick(&c, &st, 0);
    distance_ticks(&c, &st, &now, 1u, 60000u);

    /* Integrated exactly, 0.005 km/h is 83 mm a minute of pure fiction.
     * DIST_MIN_MMH is what stops it, and the truncation used to by luck. */
    TT_EQ(c.total_mm, 0);
}

/* --- range -------------------------------------------------------------- */

static void test_range_uses_the_default_until_five_km(void)
{
    compute_t c;
    compute_init(&c);
    c.tank_damped_ml = 40000;               /* 40 l */
    c.tank_damped_valid = true;
    c.total_mm = 1000000;                   /* 1 km */
    TT_EQ(compute_range_km(&c), 444);       /* 40 l at 9.0 l/100 km */
}

static void test_range_uses_the_rolling_window_after_five_km(void)
{
    compute_t c;
    uint8_t i;
    compute_init(&c);
    c.tank_damped_ml = 40000;
    c.tank_damped_valid = true;
    c.total_mm = 10000000;                  /* 10 km */
    for (i = 0; i < 10; i++) {
        c.seg_ul[i] = 60000;                /* 60 ml/km = 6.0 l/100 km */
    }
    c.seg_count = 10;
    TT_EQ(compute_range_km(&c), 666);       /* 40 l at 6.0 l/100 km */
}

/* Two more range tests live in the tank section below, where the helper that
 * drives the damping filter is defined: test_range_ignores_the_slosh and
 * test_range_falls_as_fuel_is_burnt. */

/* --- torque and power --------------------------------------------------- */

/* The drag line is fitted on the four warm free-revving holds, 13 to 16. All
 * four are stationary in neutral, so the crank drives nothing and the net
 * torque is zero at each -- which is what makes them a calibration and not
 * just data. The line is a least-squares fit rather than a two-point
 * interpolation, so the residuals are real: up to 1.8 counts of b7, about
 * 1.3 Nm. The test asserts that, rather than an exact zero it cannot have. */
static void test_drag_model_sits_on_the_warm_free_rev_holds(void)
{
    decode_state_t st;
    decode_init(&st);

    /* Each hold was stationary but with the throttle held open, 48 to 61, so
     * the idle gate does NOT apply here and the drag line answers on its own.
     * That is the point of running these four through it. */
    st.speed_mmh = 5u;

    /* 13_rev1500_z1, oil 72.8 C. Model is above the point, so it clamps. */
    st.rpm_q4 = 1536u * 4u;
    st.torque_ind_cnm = 19u * TORQUE_CNM_PER_BIT;
    st.throttle = 48u;
    TT_EQ(compute_torque_d(&st), 0);

    /* 14_rev1850_z1, oil 74.2 C. */
    st.rpm_q4 = 1850u * 4u;
    st.torque_ind_cnm = 21u * TORQUE_CNM_PER_BIT;
    st.throttle = 51u;
    TT_EQ(compute_torque_d(&st), 0);

    /* 15_rev2372_z1, oil 75.3 C. The one point the line falls below, by the
     * fit's largest residual. 1.3 Nm of phantom torque, and no more. */
    st.rpm_q4 = 2372u * 4u;
    st.torque_ind_cnm = 26u * TORQUE_CNM_PER_BIT;
    st.throttle = 56u;
    TT_TRUE(compute_torque_d(&st) <= 15u);

    /* 16_rev2926_z1, oil 76.6 C. */
    st.rpm_q4 = 2926u * 4u;
    st.torque_ind_cnm = 27u * TORQUE_CNM_PER_BIT;
    st.throttle = 61u;
    TT_EQ(compute_torque_d(&st), 0);
}

/* compute_power_d() takes the torque the caller already has, because
 * txframes_gather transmits both and used to work it out twice. Every test
 * below wants "the power for this bus state", so the pairing lives here once
 * rather than at nineteen call sites. */
static uint16_t power_d(const decode_state_t *st)
{
    return compute_power_d(st, compute_torque_d(st));
}

/* ===================================================================== *
 *  THE IDLE GATE -- A FIXED REQUIREMENT, NOT A CALIBRATION.
 *
 *  A car standing still with the throttle shut displays ZERO torque and
 *  ZERO power. Cold or hot, whatever idle speed the ECU picks, whatever a
 *  future refit does to the drag line. These tests exist so that the rule
 *  cannot be relaxed by accident: if one of them goes red, the fix is the
 *  code, NOT the test.
 *
 *  The drag line cannot deliver this on its own. In neutral net torque is
 *  zero at idle and at every free-revving hold, but b7 falls 24.96 -> 18.81
 *  between 798 and 1536 rpm, so no straight line in rpm passes through both.
 *  One of the two has to be asserted. See config.h.
 * ===================================================================== */

static void test_idle_gate_zero_at_a_standstill_warm(void)
{
    decode_state_t st;
    decode_init(&st);

    /* 11_idle_noac_z1: 798 rpm, b7 = 25, oil 72.8 C, A/C off, standing. */
    st.rpm_q4 = 798u * 4u;
    st.torque_ind_cnm = 25u * TORQUE_CNM_PER_BIT;
    st.speed_mmh = 5u;                  /* raw 1 -- what standing really sends */
    st.throttle = THROTTLE_REST;
    TT_EQ(compute_torque_d(&st), 0);
    TT_EQ(power_d(&st), 0);
}

static void test_idle_gate_zero_at_a_standstill_cold(void)
{
    decode_state_t st;
    decode_init(&st);

    /* 02_idle_60s: b7 = 29 on 60.8 C oil. Without the gate the cold engine is
     * the worse case -- 10.9 Nm -- which is exactly why the gate is not a
     * tolerance on the drag fit. */
    st.rpm_q4 = 797u * 4u;
    st.torque_ind_cnm = 29u * TORQUE_CNM_PER_BIT;
    st.speed_mmh = 5u;
    st.throttle = THROTTLE_REST;
    TT_EQ(compute_torque_d(&st), 0);
    TT_EQ(power_d(&st), 0);
}

/* A cold engine idles fast. 06_trip_reset reaches 1310 rpm standing still with
 * the throttle at rest, so the gate must not be a narrow window around 800. */
static void test_idle_gate_covers_a_fast_cold_idle(void)
{
    decode_state_t st;
    decode_init(&st);
    st.speed_mmh = 5u;
    st.throttle = THROTTLE_REST;

    st.rpm_q4 = 1310u * 4u;
    st.torque_ind_cnm = 60u * TORQUE_CNM_PER_BIT;
    TT_EQ(compute_torque_d(&st), 0);

    /* 17_drive_property_z1 reaches 1449 rpm standing with the throttle shut,
     * coming down off a blip. Still zero. */
    st.rpm_q4 = 1449u * 4u;
    st.torque_ind_cnm = 47u * TORQUE_CNM_PER_BIT;
    TT_EQ(compute_torque_d(&st), 0);
}

/* The gate must let go the moment the driver asks for anything, or pulling
 * away would read zero. Throttle above rest with the car still stationary is
 * exactly the clutch biting, and that is real torque. */
static void test_idle_gate_releases_on_throttle_while_still_stationary(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 1338u * 4u;             /* 03_drive, pulling away */
    st.torque_ind_cnm = 57u * TORQUE_CNM_PER_BIT;
    st.speed_mmh = 5u;                  /* still reading 1 on the bus */
    st.throttle = 48u;                  /* but the pedal has moved */
    TT_TRUE(compute_torque_d(&st) > 0u);
}

/* ...and it must let go once the car moves, even with the throttle shut.
 * Coasting downhill off the throttle is not a standstill. Whether the torque
 * is then zero is the drag line's business, not the gate's -- what this pins
 * is that the gate itself is no longer the reason. */
static void test_idle_gate_releases_once_the_car_moves(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 2500u * 4u;
    st.torque_ind_cnm = 120u * TORQUE_CNM_PER_BIT;
    st.speed_mmh = 40000u;              /* 40 km/h */
    st.throttle = THROTTLE_REST;
    TT_TRUE(compute_torque_d(&st) > 0u);
}

/* The threshold is not an equality, because a standing car does not send zero:
 * 0x1A0 raw speed is 1 in every log while stationary. Both must gate. */
static void test_idle_gate_thresholds_are_not_equalities(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 798u * 4u;
    st.torque_ind_cnm = 29u * TORQUE_CNM_PER_BIT;
    st.throttle = THROTTLE_REST;

    st.speed_mmh = 0u;                  /* engine off / no reading yet */
    TT_EQ(compute_torque_d(&st), 0);
    st.speed_mmh = 5u;                  /* raw 1, the real standing value */
    TT_EQ(compute_torque_d(&st), 0);
    st.speed_mmh = IDLE_GATE_SPEED_MMH; /* the boundary itself gates */
    TT_EQ(compute_torque_d(&st), 0);
    st.speed_mmh = IDLE_GATE_SPEED_MMH + 1u;
    TT_TRUE(compute_torque_d(&st) > 0u);
}

static void test_torque_above_drag(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 3000u * 4u;
    st.torque_ind_cnm = 15000;              /* 150.00 Nm indicated */
    st.speed_mmh = 60000u;                  /* moving, so the idle gate is out */
    st.throttle = 90u;
    /* drag at 3000 rpm = 6.74 + 14.46 = 21.20 Nm, so 128.80 net */
    TT_NEAR(compute_torque_d(&st), 1288, 2);
}

static void test_power(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 3000u * 4u;
    st.torque_ind_cnm = 15000;
    st.speed_mmh = 60000u;
    st.throttle = 90u;
    /* 128.80 Nm at 3000 rpm = 40.5 kW */
    TT_NEAR(power_d(&st), 405, 2);
}

static void test_engine_off_makes_no_torque(void)
{
    decode_state_t st;
    decode_init(&st);
    TT_EQ(compute_torque_d(&st), 0);
    TT_EQ(power_d(&st), 0);
}

/* THE CEILING. b7 is one byte, so the model has a hard maximum whatever the
 * engine does, and nothing in the firmware used to check that the maximum was
 * high enough to show what the car is sold as. It was not: at 0.67 Nm/bit the
 * display topped out at 76.5 kW and 147 Nm, so the factory 85 kW could not
 * appear at any throttle opening. These two tests exist so that a change to
 * TORQUE_CNM_PER_BIT or to the drag line cannot put the ratings out of reach
 * again without a red test.
 *
 * The AQY is rated 85 kW at 5200 rpm and 170 Nm at 2400 rpm. The tolerance is
 * 5 %: the scale is a decision, not a measurement, so pinning it exactly would
 * only pin the guess. On the warm drag line the two ratings agree on a 0.736
 * to 0.738 Nm/bit bracket and 0.74 delivers 85.4 kW and 170.4 Nm -- both now
 * land just ABOVE the ratings rather than 3 % below, which is what the refit
 * was for. See config.h. */
static void test_full_scale_reaches_the_rated_power(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 5200u * 4u;
    st.torque_ind_cnm = 255u * TORQUE_CNM_PER_BIT;
    st.speed_mmh = 120000u;                 /* full scale means moving fast */
    st.throttle = 211u;                     /* and the pedal on the floor    */
    TT_TRUE(power_d(&st) >= 850u - 43u);       /* 85.0 kW, -5 % */
}

static void test_full_scale_reaches_the_rated_torque(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 2400u * 4u;
    st.torque_ind_cnm = 255u * TORQUE_CNM_PER_BIT;
    st.speed_mmh = 80000u;
    st.throttle = 211u;
    TT_TRUE(compute_torque_d(&st) >= 1700u - 85u);     /* 170.0 Nm, -5 % */
}

/* 06_trip_reset holds b7 = 191-192 through the whole start, while rpm climbs
 * from 187 to 881. Without the cranking gate that is ~125 Nm and ~9 kW on the
 * display at every start. */
static void test_cranking_is_not_torque(void)
{
    decode_state_t st;
    decode_init(&st);
    st.torque_ind_cnm = 192u * TORQUE_CNM_PER_BIT;

    /* Throttle open and the car rolling, so that what is under test here is
     * the CRANKING gate alone and not the idle gate, which would otherwise
     * hide it by returning zero for its own reasons. */
    st.speed_mmh = 20000u;
    st.throttle = 60u;

    st.rpm_q4 = 288u * 4u;                  /* starter turning it over */
    TT_EQ(compute_torque_d(&st), 0);
    TT_EQ(power_d(&st), 0);

    st.rpm_q4 = 797u * 4u;                  /* running -- the gate is clear */
    TT_TRUE(compute_torque_d(&st) > 0u);
}

/* --- tank, median and the refuelling reset ------------------------------ */

/* Feed n seconds of ticks with a fixed tank reading and speed. */
static void tank_seconds(compute_t *c, decode_state_t *st, uint32_t *now,
                         uint8_t litres, uint32_t speed_mmh, int seconds)
{
    int i;
    st->tank_l = litres;
    st->speed_mmh = speed_mmh;
    st->speed_valid = true;
    for (i = 0; i < seconds; i++) {
        *now += TANK_SAMPLE_MS;
        compute_tick(c, st, *now);
    }
}

/* The bug this replaced: range read the raw float position, so on 07_accel it
 * swung over 111 km several times a second during a pull-away, while the level
 * gauge beside it -- damped all along -- sat still. */
static void test_range_ignores_the_slosh(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    uint16_t first, last;
    int i;

    compute_init(&c);
    decode_init(&st);
    c.total_mm = 1000000;                   /* 1 km, so the 9.0 default */

    tank_seconds(&c, &st, &now, 30, 0, 400);        /* settle at 30 l, standing */
    first = compute_range_km(&c);
    TT_EQ(first, 333);                              /* 30 l at 9.0 l/100 km */

    for (i = 0; i < 60; i++) {                      /* a minute of +/- 5 l */
        tank_seconds(&c, &st, &now, (uint8_t)(i & 1 ? 35 : 25), 50000, 1);
    }
    last = compute_range_km(&c);
    /* Reading st->tank_l would have alternated between 277 and 388 km. */
    TT_TRUE(last + 12u > first && last < first + 12u);
}

/* Range has to follow the tank down over a long drive. The stable median would
 * not -- it only updates at rest, so a motorway run would freeze it. */
static void test_range_falls_as_fuel_is_burnt(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    uint16_t before, after;

    compute_init(&c);
    decode_init(&st);
    c.total_mm = 1000000;

    tank_seconds(&c, &st, &now, 30, 0, 400);
    before = compute_range_km(&c);
    tank_seconds(&c, &st, &now, 20, 50000, 1200);   /* 20 min at 50 km/h */
    after = compute_range_km(&c);
    TT_TRUE(after < before);
    TT_NEAR(after, 222, 20);                        /* 20 l at 9.0 l/100 km */
}

static void test_first_stable_reading_only_initialises(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    compute_init(&c);
    decode_init(&st);
    c.total_ul = 500000;
    c.total_mm = 8000000;
    compute_tick(&c, &st, now);
    tank_seconds(&c, &st, &now, 40, 0, 10);
    TT_TRUE(c.tank_stable_valid);
    TT_EQ(c.tank_stable_l, 40);
    /* Resetting here would clear the average on every power-up. */
    TT_EQ(c.refuels, 0);
    TT_EQ(c.total_ul, 500000);
}

static void test_refuelling_clears_the_average(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    compute_init(&c);
    decode_init(&st);
    compute_tick(&c, &st, now);
    tank_seconds(&c, &st, &now, 10, 0, 30);
    c.total_ul = 500000;
    c.total_mm = 8000000;

    tank_seconds(&c, &st, &now, 45, 0, 30);     /* somebody filled up */
    TT_EQ(c.refuels, 1);
    TT_EQ(c.total_ul, 0);
    TT_EQ(c.total_mm, 0);
    TT_EQ(c.tank_stable_l, 45);
}

/* A refuelling is the one tank change that is both large and instantaneous,
 * and the one moment the driver certainly looks at the gauge. Crawling up to
 * it with a time constant of minutes would show a stale level and a stale
 * range for minutes after filling up. */
static void test_refuelling_snaps_the_damped_level(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    compute_init(&c);
    decode_init(&st);
    compute_tick(&c, &st, now);
    tank_seconds(&c, &st, &now, 10, 0, 30);
    TT_NEAR(compute_tank_d(&c), 100, 2);

    tank_seconds(&c, &st, &now, 45, 0, 15);     /* fill up, still standing */
    TT_EQ(c.refuels, 1);
    /* Not 10 l plus a fortnight of filter. */
    TT_NEAR(compute_tank_d(&c), 450, 20);
}

static void test_a_small_rise_is_not_refuelling(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    compute_init(&c);
    decode_init(&st);
    compute_tick(&c, &st, now);
    tank_seconds(&c, &st, &now, 10, 0, 30);
    c.total_ul = 500000;

    tank_seconds(&c, &st, &now, 13, 0, 30);     /* +3 L, at the threshold */
    TT_EQ(c.refuels, 0);
    TT_EQ(c.total_ul, 500000);
}

static void test_sloshing_while_driving_is_ignored(void)
{
    /* In 07_accel the level jumps between 1, 5, 7 and 9 litres during a short
     * pull-away. Tied to the instantaneous value, the reset would fire on
     * every one of them. */
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    compute_init(&c);
    decode_init(&st);
    compute_tick(&c, &st, now);
    tank_seconds(&c, &st, &now, 6, 0, 30);
    c.total_ul = 500000;

    tank_seconds(&c, &st, &now, 30, 40000, 60); /* 40 km/h, tank "jumps" */
    TT_EQ(c.refuels, 0);
    TT_EQ(c.tank_stable_l, 6);
    TT_EQ(c.total_ul, 500000);
}

/* The counter is what replaced the median's rejection of outliers, so this is
 * the test that says it actually rejects them: four seconds of a high reading
 * with one ordinary sample in the middle is not a refuelling, however high the
 * reading is. A median of 25 would have needed thirteen such samples; this
 * needs five in a row. */
static void test_a_single_high_reading_is_not_refuelling(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    int i;

    compute_init(&c);
    decode_init(&st);
    compute_tick(&c, &st, now);
    tank_seconds(&c, &st, &now, 10, 0, 30);
    c.total_ul = 500000;

    for (i = 0; i < 20; i++) {
        tank_seconds(&c, &st, &now, 40, 0, 4);      /* four high ...        */
        tank_seconds(&c, &st, &now, 10, 0, 1);      /* ... and one sane     */
    }
    TT_EQ(c.refuels, 0);
    TT_EQ(c.total_ul, 500000);

    /* And the baseline did not creep upwards while all that was going on --
     * it is frozen for as long as the counter is running. */
    TT_EQ(c.tank_stable_l, 10);
}

/* The normal case: refuelling happens with the ignition off, so the rise is
 * seen against what came out of the EEPROM on the next start. */
static void test_refuelling_is_detected_across_an_ignition_cycle(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;

    compute_init(&c);
    decode_init(&st);
    /* What persist.c read back: 8 l in the tank, half a trip driven. */
    compute_restore(&c, 500000, 8000000, 8, true);
    compute_tick(&c, &st, now);

    /* Ignition on at the pump, tank now full. Five seconds at rest. */
    tank_seconds(&c, &st, &now, 45, 0, (int)REFUEL_CONFIRM_S);
    TT_EQ(c.refuels, 1);
    TT_EQ(c.total_ul, 0);
    TT_EQ(c.total_mm, 0);
    TT_EQ(c.tank_stable_l, 45);
}

/* No fixture contains a refuelling -- the tank reads 0 l with the reserve lamp
 * on through most of them -- so none of them may produce one either. A false
 * positive silently destroys an average the driver has watched for 600 km,
 * which is the asymmetry docs/refuel-reset.md is built around, and the sender
 * jumping between 1, 5, 7 and 9 l during a pull-away is exactly the shape of
 * input that could cause one. */
static void test_no_fixture_triggers_a_refuelling(void)
{
    static const char *logs[] = {
        "01_ign_only.txt", "02_idle_60s.txt", "03_drive.txt",
        "05_rev3000.txt", "06_trip_reset.txt", "07_accel.txt",
        "08_ign_only_z1.txt", "09_idle_60s_z1.txt", "10_rev2600_z1.txt",
        "11_idle_noac_z1.txt", "12_idle_ac_z1.txt", "13_rev1500_z1.txt",
        "14_rev1850_z1.txt", "15_rev2372_z1.txt", "16_rev2926_z1.txt",
        "17_drive_property_z1.txt", "idle.txt" };
    size_t i;
    for (i = 0; i < sizeof logs / sizeof logs[0]; i++) {
        replay_result_t r;
        TT_TRUE(replay_log(logs[i], &r));
        TT_EQ(r.cp.refuels, 0);
    }
}

static void test_tank_is_damped(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    compute_init(&c);
    decode_init(&st);
    compute_tick(&c, &st, now);
    tank_seconds(&c, &st, &now, 40, 0, 5);
    TT_EQ(compute_tank_d(&c), 400);             /* first sample seeds it */

    tank_seconds(&c, &st, &now, 20, 0, 5);
    /* Five seconds into a TANK_DAMP_SAMPLES time constant it has barely
     * moved. A fall is not a refuelling, so nothing snaps it. */
    TT_RANGE(compute_tank_d(&c), 380, 400);
    tank_seconds(&c, &st, &now, 20, 0, 900);
    TT_NEAR(compute_tank_d(&c), 200, 2);
}

/* --- liveness ----------------------------------------------------------- */

static void test_data_timeout(void)
{
    compute_t c;
    decode_state_t st = running(1000, 800);
    compute_init(&c);
    TT_FALSE(compute_data_live(&c, 0));
    compute_on_fuel(&c, &st, 1000);
    TT_TRUE(compute_data_live(&c, 1000));
    TT_TRUE(compute_data_live(&c, 1000 + DATA_TIMEOUT_MS));
    TT_FALSE(compute_data_live(&c, 1001 + DATA_TIMEOUT_MS));
}

/* --- against the real logs ---------------------------------------------- */

static void test_idle_totals(void)
{
    replay_result_t r;
    TT_TRUE(replay_log("02_idle_60s.txt", &r));
    TT_EQ(r.cp.total_ul, 18652);
    TT_EQ(r.cp.total_mm, 0);
    TT_EQ(r.cp.restarts, 0);
    /* 18,652 ul over 60.1 s = 310 ul/s = 1.12 l/h */
    TT_NEAR(r.span_ms, 60100, 100);
    TT_NEAR(r.cp.total_ul * 1000u / r.span_ms, 310, 2);
}

static void test_idle_instantaneous_flow(void)
{
    replay_result_t r;
    TT_TRUE(replay_log("02_idle_60s.txt", &r));
    /* The sliding window at the end of a minute of steady idling must agree
     * with the average over the whole minute. */
    TT_NEAR(r.cp.flow_ul_s, 310, 40);
    TT_NEAR(compute_flow_lh_c(&r.cp), 112, 15);     /* 1.12 l/h */
}

static void test_ign_only_burns_nothing_and_moves_nothing(void)
{
    replay_result_t r;
    TT_TRUE(replay_log("01_ign_only.txt", &r));
    TT_EQ(r.cp.total_ul, 0);
    TT_EQ(r.cp.total_mm, 0);
    TT_EQ(r.cp.flow_ul_s, 0);
}

static void test_rev3000_totals(void)
{
    replay_result_t r;
    TT_TRUE(replay_log("05_rev3000.txt", &r));
    TT_EQ(r.cp.total_ul, 1940);
    TT_NEAR(r.span_ms, 1930, 30);
    TT_NEAR(r.cp.total_ul * 1000u / r.span_ms, 1005, 20);
}

static void test_trip_reset_distance_matches_the_checklist(void)
{
    /* The checklist said "drive at least 0.1 km". It came out as 125 m. */
    replay_result_t r;
    TT_TRUE(replay_log("06_trip_reset.txt", &r));
    TT_EQ(r.cp.total_ul, 51992);
    TT_RANGE(r.cp.total_mm, 100000, 200000);
}

static void test_accel_distance_needs_the_corrected_gate(void)
{
    /* With b1 == 0x40 as an equality this would be 14 m instead of 27 m. */
    replay_result_t r;
    TT_TRUE(replay_log("07_accel.txt", &r));
    TT_EQ(r.cp.total_ul, 9752);
    TT_TRUE(r.cp.total_mm > 20000);
    TT_EQ(r.cp.restarts, 0);
}

static void test_restart_detection_covers_the_engine_off_prefix(void)
{
    /* 06 opens with the ignition on but the engine not running, so there are
     * many restarts -- and that is correct. They all fall in the opening
     * stretch, not in the middle of driving. */
    replay_result_t r;
    TT_TRUE(replay_log("06_trip_reset.txt", &r));
    TT_TRUE(r.cp.restarts > 300);
}

static void test_average_stays_sane_on_every_log(void)
{
    /* Trap 4 in one line: no log may produce a runaway average. */
    static const char *logs[] = { "01_ign_only.txt", "02_idle_60s.txt",
                                  "03_drive.txt", "05_rev3000.txt",
                                  "06_trip_reset.txt", "07_accel.txt",
                                  "idle.txt" };
    size_t i;
    for (i = 0; i < sizeof logs / sizeof logs[0]; i++) {
        replay_result_t r;
        TT_TRUE(replay_log(logs[i], &r));
        TT_TRUE(compute_avg_l100_d(&r.cp) < FUELNOW_CLAMP_D);
    }
}

int main(void)
{
    printf("test_compute\n");
    TT_RUN(test_normal_delta);
    TT_RUN(test_wrap_at_32768);
    TT_RUN(test_ignition_off_does_not_produce_a_jump);
    TT_RUN(test_engine_stopped_resets_reference);
    TT_RUN(test_engine_stopped_zeroes_the_flow);

    TT_RUN(test_below_threshold_is_litres_per_hour);
    TT_RUN(test_at_threshold_switches_unit);
    TT_RUN(test_no_hysteresis);
    TT_RUN(test_clamped_to_999);
    TT_RUN(test_invalid_speed_falls_back_to_flow);
    TT_RUN(test_zero_flow);
    TT_RUN(test_documented_table);

    TT_RUN(test_average_below_minimum_distance_is_zero);
    TT_RUN(test_average_is_a_ratio_of_accumulators);
    TT_RUN(test_idling_does_not_ruin_the_average);

    TT_RUN(test_distance_does_not_depend_on_the_tick_rate);
    TT_RUN(test_walking_pace_still_covers_ground);
    TT_RUN(test_a_standing_car_covers_no_distance);

    TT_RUN(test_range_uses_the_default_until_five_km);
    TT_RUN(test_range_uses_the_rolling_window_after_five_km);

    TT_RUN(test_drag_model_sits_on_the_warm_free_rev_holds);
    TT_RUN(test_idle_gate_zero_at_a_standstill_warm);
    TT_RUN(test_idle_gate_zero_at_a_standstill_cold);
    TT_RUN(test_idle_gate_covers_a_fast_cold_idle);
    TT_RUN(test_idle_gate_releases_on_throttle_while_still_stationary);
    TT_RUN(test_idle_gate_releases_once_the_car_moves);
    TT_RUN(test_idle_gate_thresholds_are_not_equalities);
    TT_RUN(test_torque_above_drag);
    TT_RUN(test_power);
    TT_RUN(test_engine_off_makes_no_torque);
    TT_RUN(test_full_scale_reaches_the_rated_power);
    TT_RUN(test_full_scale_reaches_the_rated_torque);
    TT_RUN(test_cranking_is_not_torque);

    TT_RUN(test_range_ignores_the_slosh);
    TT_RUN(test_range_falls_as_fuel_is_burnt);

    TT_RUN(test_first_stable_reading_only_initialises);
    TT_RUN(test_refuelling_clears_the_average);
    TT_RUN(test_refuelling_snaps_the_damped_level);
    TT_RUN(test_a_small_rise_is_not_refuelling);
    TT_RUN(test_sloshing_while_driving_is_ignored);
    TT_RUN(test_a_single_high_reading_is_not_refuelling);
    TT_RUN(test_refuelling_is_detected_across_an_ignition_cycle);
    TT_RUN(test_no_fixture_triggers_a_refuelling);
    TT_RUN(test_tank_is_damped);

    TT_RUN(test_data_timeout);

    TT_RUN(test_idle_totals);
    TT_RUN(test_idle_instantaneous_flow);
    TT_RUN(test_ign_only_burns_nothing_and_moves_nothing);
    TT_RUN(test_rev3000_totals);
    TT_RUN(test_trip_reset_distance_matches_the_checklist);
    TT_RUN(test_accel_distance_needs_the_corrected_gate);
    TT_RUN(test_restart_detection_covers_the_engine_off_prefix);
    TT_RUN(test_average_stays_sane_on_every_log);
    return TT_SUMMARY();
}
