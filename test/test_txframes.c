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
    /* Moving with the throttle open, so the idle gate is not what this test
     * is measuring -- it is the bus-quiet timeout below. */
    st.speed_mmh = 60000u;
    st.throttle = 90u;
    st.tank_l = 40;
    st.tank_valid = true;
    st.fuel_counter_valid = true;
    st.fuel_counter = 1000;
    /* Range reads the damped level, which compute_tick fills in. */
    c.tank_damped_ml = 40000;
    c.tank_damped_valid = true;

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

/* The trip totals are gathered in the slow slot, not in the fast one -- 0x602
 * goes out once a second and computing them ten times a second was two
 * divisions by 1000 for nobody to read. They obey the same quiet-bus rule as
 * everything else, which is the half of it that is easy to lose in the move. */
static void test_trip_totals_are_gathered_for_the_slow_frame(void)
{
    compute_t c;
    decode_state_t st;
    tx_values_t v;

    compute_init(&c);
    decode_init(&st);
    st.fuel_counter_valid = true;
    st.fuel_counter = 1000;
    st.rpm_q4 = 800u * 4u;
    compute_on_fuel(&c, &st, 1000);
    c.total_ul = 7654321u;              /* 7654.321 ml */
    c.total_mm = 12345678u;             /* 12345.678 m */

    /* The fast gather does not touch them any more. */
    txframes_gather(&v, &c, &st, 503, 1000);
    TT_EQ(v.trip_ml, 0);
    TT_EQ(v.trip_m, 0);

    txframes_gather_trip(&v, &c, 1000);
    TT_EQ(v.trip_ml, 7654u);
    TT_EQ(v.trip_m, 12345u);

    /* And a bus that has gone quiet zeroes them, exactly as the gather does
     * with everything else derived from it. */
    txframes_gather_trip(&v, &c, 1000 + DATA_TIMEOUT_MS + 1u);
    TT_EQ(v.trip_ml, 0);
    TT_EQ(v.trip_m, 0);
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
    st.tank_valid = true;
    c.tank_damped_ml = 40000;           /* range reads the damped level */
    c.tank_damped_valid = true;
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
    TT_NEAR(be16(f + 0), 405, 2);       /* 40.5 kW  */
    TT_NEAR(be16(f + 2), 1288, 2);      /* 128.8 Nm */
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

    /* Standing still, so FuelNow is in l/h: an idle flow, never l/100 km.
     * The window is four quarter-second buckets read wherever the last one
     * closed, so the exact digit depends on where in the log that fell --
     * test_compute.c says the same thing at more length. */
    TT_RANGE(be16(f + 0), 9, 16);
    /* The car never moved, so the average must be exactly zero and not a
     * division by an almost-zero distance. */
    TT_EQ(be16(f + 2), 0);

    txframes_engine(&v, f);
    TT_RANGE(be16(f + 4), 90, 162);     /* 0.90 to 1.62 l/h at idle */

    /* IDLING PRODUCES NO NET TORQUE AND THE DISPLAY MUST SAY SO -- end to end,
     * off a real log, through decode, compute and the assembled frame. This is
     * the idle gate (config.h) and it is a fixed requirement, not a tolerance
     * on the drag fit: 02_idle_60s is the worst case for it, b7 = 29 on 60.8 C
     * oil, which the drag line alone would show as 10.9 Nm. Zero here, and
     * zero at the two warm idle logs below.
     *
     * IF THIS GOES RED, FIX THE CODE, NOT THE TEST. */
    TT_EQ(be16(f + 2), 0);              /* torque */
    TT_EQ(be16(f + 0), 0);              /* power  */
}

/* The same end to end on the two warm idle recordings, one with the air
 * conditioning running -- a real load on the engine that raises b7 from 25 to
 * 42 and still must not put a number on the display, because the car is not
 * going anywhere. */
static void test_warm_idle_logs_also_show_zero_torque(void)
{
    static const char *const logs[] = { "11_idle_noac_z1.txt",
                                        "12_idle_ac_z1.txt",
                                        "09_idle_60s_z1.txt" };
    size_t i;

    for (i = 0; i < sizeof logs / sizeof logs[0]; i++) {
        replay_result_t r;
        tx_values_t v;
        uint8_t f[TXFRAME_DLC];

        TT_TRUE(replay_log(logs[i], &r));
        txframes_gather(&v, &r.cp, &r.st, 500, r.cp.last_data_ms);
        txframes_engine(&v, f);
        TT_EQ(be16(f + 2), 0);          /* torque */
        TT_EQ(be16(f + 0), 0);          /* power  */
    }
}

static void test_every_log_stays_inside_the_gauges(void)
{
    /* The TRI gauges top out at 99.90 for FuelNow and FuelAvg. Anything
     * above behaves unpredictably on the display, so nothing may leave here
     * above the clamp.
     *
     * This is the only all-logs sweep of the clamp left. test_compute.c had a
     * second one that asserted the average alone over the same seven logs --
     * a strict subset of these two lines, so it does not belong here.
     * Trap 4 itself is pinned precisely by
     * test_average_below_minimum_distance_is_zero, and the clamp over a state
     * space no fixture reaches by test_props.c. */
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

/* 0x603 is ours alone -- S-AQY.TRI does not read it -- so these offsets are
 * pinned against docs/frames.md and against tools/bench_test.py, which decodes
 * them on the bench. Nothing on the display breaks if they move; the bench
 * test silently starts lying, which is worse. */
static void test_diag_frame_offsets(void)
{
    tx_values_t v;
    uint8_t out[TXFRAME_DLC];

    memset(&v, 0, sizeof v);
    txframes_gather_diag(&v, 0x11u, 0x22u, 0x33u, 0x1Fu,
                         RESET_CAUSE_WATCHDOG, 0x44u, 0x5566u);
    txframes_diag(&v, out);

    TT_EQ(out[0], 0x11u);               /* rx error counter        */
    TT_EQ(out[1], 0x22u);               /* tx error counter        */
    TT_EQ(out[2], 0x33u);               /* COMSTAT                 */
    TT_EQ(out[3], 0x1Fu);               /* our flags               */
    TT_EQ(out[5], 0x44u);               /* send refusals           */
    TT_EQ(be16(out + 6), 0x5566u);      /* uptime, seconds         */

    /* b4 is shared: reset cause in the low five bits, layout version in the
     * top three. Both halves are checked, because a shift that moved would
     * still leave one of them looking right. */
    TT_EQ(out[4] & DIAG_RESET_CAUSE_MASK, RESET_CAUSE_WATCHDOG);
    TT_EQ(out[4] >> DIAG_VERSION_SHIFT, DIAG_LAYOUT_VERSION);
}

/* Five causes have to survive the mask that shares their byte with the
 * version. RESET_CAUSE_STACK is bit 4 and is the one that would be silently
 * eaten if the split ever moved back to a nibble. */
static void test_every_reset_cause_survives_the_shared_byte(void)
{
    static const uint8_t causes[] = {
        RESET_CAUSE_POWER_ON, RESET_CAUSE_BROWN_OUT, RESET_CAUSE_WATCHDOG,
        RESET_CAUSE_RESET_INSTR, RESET_CAUSE_STACK
    };
    size_t i;

    for (i = 0; i < sizeof causes / sizeof causes[0]; i++) {
        tx_values_t v;
        uint8_t out[TXFRAME_DLC];

        memset(&v, 0, sizeof v);
        txframes_gather_diag(&v, 0u, 0u, 0u, 0u, causes[i], 0u, 0u);
        txframes_diag(&v, out);

        TT_EQ(out[4] & DIAG_RESET_CAUSE_MASK, causes[i]);
        TT_EQ(out[4] >> DIAG_VERSION_SHIFT, DIAG_LAYOUT_VERSION);
    }
}

/* The other two gathers zero everything when the bus goes quiet, so that a
 * driver never reads a stale number. The diagnostic frame must not: it is the
 * one frame whose whole job is to keep reporting when things have gone wrong,
 * and a quiet bus is one of the things that can be wrong. */
static void test_diag_does_not_zero_on_a_quiet_bus(void)
{
    compute_t c;
    tx_values_t v;
    uint8_t out[TXFRAME_DLC];

    compute_init(&c);
    memset(&v, 0, sizeof v);

    /* Same call order main.c uses in the slow slot, with a clock far past
     * DATA_TIMEOUT_MS so compute_data_live() is false. */
    txframes_gather_trip(&v, &c, 10u * DATA_TIMEOUT_MS);
    txframes_gather_diag(&v, 7u, 9u, 0x20u, DIAG_FLAG_CAN_OK, 0u, 3u, 42u);
    txframes_diag(&v, out);

    TT_EQ(out[0], 7u);
    TT_EQ(out[1], 9u);
    TT_EQ(out[2], 0x20u);               /* COMSTAT TXBO, still reported  */
    TT_EQ(out[3], DIAG_FLAG_CAN_OK);
    TT_EQ(out[5], 3u);
    TT_EQ(be16(out + 6), 42u);
}

/* The five flags must stay one bit each and must not overlap: the whole point
 * of the byte is that a reader can test one bit without masking the rest. */
static void test_diag_flags_are_distinct_bits(void)
{
    uint8_t all = (uint8_t)(DIAG_FLAG_CAN_OK | DIAG_FLAG_SILENT |
                            DIAG_FLAG_UNHEALTHY | DIAG_FLAG_DATA_LIVE |
                            DIAG_FLAG_PERSIST_OK);
    unsigned bits = 0u;
    unsigned i;

    for (i = 0u; i < 8u; i++) {
        if (all & (1u << i)) {
            bits++;
        }
    }
    TT_EQ(bits, 5u);
}

int main(void)
{
    printf("test_txframes\n");
    TT_RUN(test_fuel_frame_offsets);
    TT_RUN(test_big_endian_not_little);
    TT_RUN(test_engine_frame_offsets);
    TT_RUN(test_trip_frame_offsets);
    TT_RUN(test_gather_zeroes_when_the_bus_is_quiet);
    TT_RUN(test_trip_totals_are_gathered_for_the_slow_frame);
    TT_RUN(test_gather_fills_a_full_frame);
    TT_RUN(test_idle_produces_sane_frames);
    TT_RUN(test_warm_idle_logs_also_show_zero_torque);
    TT_RUN(test_every_log_stays_inside_the_gauges);
    TT_RUN(test_diag_frame_offsets);
    TT_RUN(test_every_reset_cause_survives_the_shared_byte);
    TT_RUN(test_diag_does_not_zero_on_a_quiet_bus);
    TT_RUN(test_diag_flags_are_distinct_bits);
    return TT_SUMMARY();
}
