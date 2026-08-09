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
    /* The table from docs/implementation-plan.md section 3.1. Flow is given
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

/* --- range -------------------------------------------------------------- */

static void test_range_uses_the_default_until_five_km(void)
{
    compute_t c;
    decode_state_t st;
    compute_init(&c);
    decode_init(&st);
    st.tank_l = 40;
    c.total_mm = 1000000;                   /* 1 km */
    TT_EQ(compute_range_km(&c, &st), 444);  /* 40 l at 9.0 l/100 km */
}

static void test_range_uses_the_rolling_window_after_five_km(void)
{
    compute_t c;
    decode_state_t st;
    uint8_t i;
    compute_init(&c);
    decode_init(&st);
    st.tank_l = 40;
    c.total_mm = 10000000;                  /* 10 km */
    for (i = 0; i < 10; i++) {
        c.seg_ul[i] = 60000;                /* 60 ml/km = 6.0 l/100 km */
    }
    c.seg_count = 10;
    TT_EQ(compute_range_km(&c, &st), 666);  /* 40 l at 6.0 l/100 km */
}

/* --- torque and power --------------------------------------------------- */

static void test_drag_model_reproduces_both_calibration_points(void)
{
    decode_state_t st;
    decode_init(&st);

    /* 02_idle_60s: 797 rpm, 0x280 b7 = 29. The engine is only driving
     * itself, so the net torque at the wheels is zero. */
    st.rpm_q4 = 797u * 4u;
    st.torque_ind_cnm = 29u * TORQUE_CNM_PER_BIT;
    TT_EQ(compute_torque_d(&st), 0);

    /* 05_rev3000: 2940 rpm in neutral, b7 = 37. Also zero at the wheels. */
    st.rpm_q4 = 2940u * 4u;
    st.torque_ind_cnm = 37u * TORQUE_CNM_PER_BIT;
    TT_EQ(compute_torque_d(&st), 0);
}

static void test_torque_above_drag(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 3000u * 4u;
    st.torque_ind_cnm = 15000;              /* 150.00 Nm indicated */
    /* drag at 3000 rpm = 17.44 + 0.75 = 25.0 Nm, so 125.0 net */
    TT_NEAR(compute_torque_d(&st), 1250, 2);
}

static void test_power(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = 3000u * 4u;
    st.torque_ind_cnm = 15000;
    /* 125 Nm at 3000 rpm = 39.3 kW */
    TT_NEAR(compute_power_d(&st), 393, 2);
}

static void test_engine_off_makes_no_torque(void)
{
    decode_state_t st;
    decode_init(&st);
    TT_EQ(compute_torque_d(&st), 0);
    TT_EQ(compute_power_d(&st), 0);
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
    /* Five seconds into a 60 s time constant it has barely moved. */
    TT_RANGE(compute_tank_d(&c), 370, 400);
    tank_seconds(&c, &st, &now, 20, 0, 300);
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

    TT_RUN(test_range_uses_the_default_until_five_km);
    TT_RUN(test_range_uses_the_rolling_window_after_five_km);

    TT_RUN(test_drag_model_reproduces_both_calibration_points);
    TT_RUN(test_torque_above_drag);
    TT_RUN(test_power);
    TT_RUN(test_engine_off_makes_no_torque);

    TT_RUN(test_first_stable_reading_only_initialises);
    TT_RUN(test_refuelling_clears_the_average);
    TT_RUN(test_a_small_rise_is_not_refuelling);
    TT_RUN(test_sloshing_while_driving_is_ignored);
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
