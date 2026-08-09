/* test_txframes.c -- the byte layout of 0x600, 0x601 and 0x602.
 *
 * These offsets are not an internal detail: mfd15/tri/S-AQY.TRI has already
 * been uploaded to a real display and reads exactly these bytes. Getting one
 * wrong produces no error anywhere, only a plausible number that is not the
 * one it claims to be. The expected offsets below are copied from the TRI
 * file itself, which lists start byte and length per sensor:
 *
 *   0600;0;0;2 FuelNow   0600;0;2;2 FuelAvg
 *   0600;0;4;2 FuelTank  0600;0;6;2 Range
 *   0601;0;0;2 Power     0601;0;2;2 Torque      0601;0;6;2 VddConv
 *
 * The third column is the format: 0 is big endian, and every one of our own
 * sensors carries a 0 while the car's carry a 1.
 */

#include <string.h>

#include "compute.h"
#include "config.h"
#include "decode.h"
#include "replay_core.h"
#include "txframes.h"
#include "tt.h"

static uint16_t be16(const uint8_t *p)
{
    return (uint16_t)(p[0] << 8 | p[1]);
}

static uint32_t be32(const uint8_t *p)
{
    return (uint32_t)p[0] << 24 | (uint32_t)p[1] << 16 |
           (uint32_t)p[2] << 8 | p[3];
}

static tx_values_t sample_values(void)
{
    tx_values_t v;
    memset(&v, 0, sizeof v);
    v.fuel_now_d  = 0x1234;
    v.fuel_avg_d  = 72;
    v.fuel_tank_d = 405;
    v.range_km    = 512;
    v.power_d     = 393;
    v.torque_d    = 1250;
    v.flow_c      = 112;
    v.vdd_c       = 503;
    v.trip_ml     = 51992u;
    v.trip_m      = 125u;
    return v;
}

/* --- 0x600 -------------------------------------------------------------- */

static void test_fuel_frame_offsets(void)
{
    tx_values_t v = sample_values();
    uint8_t f[TXFRAME_DLC];
    memset(f, 0xAA, sizeof f);
    txframes_fuel(&v, f);

    TT_EQ(be16(f + 0), v.fuel_now_d);
    TT_EQ(be16(f + 2), v.fuel_avg_d);
    TT_EQ(be16(f + 4), v.fuel_tank_d);
    TT_EQ(be16(f + 6), v.range_km);
}

static void test_big_endian_not_little(void)
{
    /* The single most likely mistake, and the one that produces numbers that
     * still look like numbers. 0x1234 must be 12 34, never 34 12. */
    tx_values_t v = sample_values();
    uint8_t f[TXFRAME_DLC];
    txframes_fuel(&v, f);
    TT_EQ(f[0], 0x12);
    TT_EQ(f[1], 0x34);
}

/* --- 0x601 -------------------------------------------------------------- */

static void test_engine_frame_offsets(void)
{
    tx_values_t v = sample_values();
    uint8_t f[TXFRAME_DLC];
    memset(f, 0xAA, sizeof f);
    txframes_engine(&v, f);

    TT_EQ(be16(f + 0), v.power_d);
    TT_EQ(be16(f + 2), v.torque_d);
    TT_EQ(be16(f + 4), v.flow_c);
    TT_EQ(be16(f + 6), v.vdd_c);
}

/* --- 0x602 -------------------------------------------------------------- */

static void test_trip_frame_offsets(void)
{
    tx_values_t v = sample_values();
    uint8_t f[TXFRAME_DLC];
    memset(f, 0xAA, sizeof f);
    txframes_trip(&v, f);

    TT_EQ(be32(f + 0), v.trip_ml);
    TT_EQ(be32(f + 4), v.trip_m);
}

/* --- gathering ---------------------------------------------------------- */

static void test_gather_zeroes_when_the_bus_is_quiet(void)
{
    compute_t c;
    decode_state_t st = { 0 };
    tx_values_t v;

    compute_init(&c);
    decode_init(&st);
    st.rpm_q4 = 3000u * 4u;
    st.torque_ind_cnm = 15000;
    st.tank_l = 40;
    st.fuel_counter_valid = true;
    st.fuel_counter = 1000;

    compute_on_fuel(&c, &st, 1000);
    txframes_gather(&v, &c, &st, 503, 1000);
    TT_TRUE(v.range_km > 0);
    TT_TRUE(v.torque_d > 0);

    /* Half a second later there has been no frame, so every bus-derived
     * value goes to zero rather than freezing at a plausible reading. */
    txframes_gather(&v, &c, &st, 503, 1000 + DATA_TIMEOUT_MS + 1u);
    TT_EQ(v.range_km, 0);
    TT_EQ(v.torque_d, 0);
    TT_EQ(v.power_d, 0);
    TT_EQ(v.fuel_now_d, 0);
    TT_EQ(v.trip_ml, 0);

    /* VddConv is ours, not the bus's, and a dead bus is exactly when you
     * want to know whether the converter is still being fed. */
    TT_EQ(v.vdd_c, 503);
}

static void test_gather_fills_a_full_frame(void)
{
    compute_t c;
    decode_state_t st;
    tx_values_t v;
    uint8_t f[TXFRAME_DLC];

    compute_init(&c);
    decode_init(&st);
    st.tank_l = 40;
    st.speed_valid = true;
    st.speed_mmh = 50000;               /* 50 km/h */
    st.rpm_q4 = 3000u * 4u;
    st.torque_ind_cnm = 15000;
    st.fuel_counter_valid = true;

    st.fuel_counter = 1000;
    compute_on_fuel(&c, &st, 0);
    st.fuel_counter = 1050;
    compute_on_fuel(&c, &st, 50);
    c.total_ul = 700000;
    c.total_mm = 10000000;

    txframes_gather(&v, &c, &st, 503, 50);
    txframes_fuel(&v, f);
    TT_EQ(be16(f + 2), 70);             /* 7.0 l/100 km average */
    TT_EQ(be16(f + 6), 444);            /* 40 l at the 9.0 default */

    txframes_engine(&v, f);
    TT_NEAR(be16(f + 0), 393, 2);       /* 39.3 kW  */
    TT_NEAR(be16(f + 2), 1250, 2);      /* 125.0 Nm */
    TT_EQ(be16(f + 6), 503);            /* 5.03 V   */
}

/* --- against a real log -------------------------------------------------- */

static void test_idle_produces_sane_frames(void)
{
    replay_result_t r;
    tx_values_t v;
    uint8_t f[TXFRAME_DLC];
    uint32_t now;

    TT_TRUE(replay_log("02_idle_60s.txt", &r));
    now = r.cp.last_data_ms;
    txframes_gather(&v, &r.cp, &r.st, 500, now);
    txframes_fuel(&v, f);

    /* Standing still, so FuelNow is in l/h: 1.1 or so, never l/100 km. */
    TT_NEAR(be16(f + 0), 11, 2);
    /* The car never moved, so the average must be exactly zero and not a
     * division by an almost-zero distance. */
    TT_EQ(be16(f + 2), 0);

    txframes_engine(&v, f);
    TT_NEAR(be16(f + 4), 112, 15);      /* 1.12 l/h */
    TT_EQ(be16(f + 2), 0);              /* idling produces no net torque */
}

static void test_every_log_stays_inside_the_gauges(void)
{
    /* The TRI gauges top out at 99.90 for FuelNow and FuelAvg. Anything
     * above behaves unpredictably on the display, so nothing may leave here
     * above the clamp. */
    static const char *logs[] = { "01_ign_only.txt", "02_idle_60s.txt",
                                  "03_drive.txt", "05_rev3000.txt",
                                  "06_trip_reset.txt", "07_accel.txt",
                                  "idle.txt" };
    size_t i;
    for (i = 0; i < sizeof logs / sizeof logs[0]; i++) {
        replay_result_t r;
        tx_values_t v;
        TT_TRUE(replay_log(logs[i], &r));
        txframes_gather(&v, &r.cp, &r.st, 500, r.cp.last_data_ms);
        TT_TRUE(v.fuel_now_d <= FUELNOW_CLAMP_D);
        TT_TRUE(v.fuel_avg_d <= FUELNOW_CLAMP_D);
    }
}

int main(void)
{
    printf("test_txframes\n");
    TT_RUN(test_fuel_frame_offsets);
    TT_RUN(test_big_endian_not_little);
    TT_RUN(test_engine_frame_offsets);
    TT_RUN(test_trip_frame_offsets);
    TT_RUN(test_gather_zeroes_when_the_bus_is_quiet);
    TT_RUN(test_gather_fills_a_full_frame);
    TT_RUN(test_idle_produces_sane_frames);
    TT_RUN(test_every_log_stays_inside_the_gauges);
    return TT_SUMMARY();
}
