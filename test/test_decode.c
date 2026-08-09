/* test_decode.c -- the C twin of TestDecode and TestSpeedGate in
 * tools/test_replay.py. Same frames, same expected numbers, only in the
 * scaled integers the firmware actually uses.
 */

#include <string.h>

#include "config.h"
#include "decode.h"
#include "logread.h"
#include "tt.h"

/* Build a frame from a hex string, the way the Python tests do. */
static void feed(decode_state_t *st, uint16_t id, const char *hex)
{
    uint8_t data[8];
    size_t n = strlen(hex) / 2;
    size_t i;
    for (i = 0; i < n && i < sizeof data; i++) {
        data[i] = (uint8_t)lr_hex2(hex + 2 * i);
    }
    decode_frame(st, id, data, (uint8_t)n);
}

/* --- the signal table --------------------------------------------------- */

static void test_rpm(void)
{
    decode_state_t st;
    decode_init(&st);
    /* b2-b3 = 90 0c -> 0x0C90 = 3216 quarters -> 804 rpm */
    feed(&st, CAN_ID_ENGINE, "0123900c25261725");
    TT_EQ(st.rpm_q4, 3216);
    TT_EQ(decode_rpm(&st), 804);
}

static void test_torque_throttle_load(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_ENGINE, "0123900c25261725");
    TT_EQ(st.throttle, 0x26);
    TT_EQ(st.load, 0x17);
    TT_EQ(st.torque_ind_cnm, 0x25 * 67);
}

static void test_clt(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_COOLANT, "8fbe3000004e2900");
    TT_EQ(st.clt_c100, 0xBE * 75 - 4800);       /* 94.50 C */
}

static void test_clt_error_value(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_COOLANT, "8fff3000004e2900");
    TT_EQ(st.clt_c100, DECODE_TEMP_INVALID);
}

static void test_oil_error_value(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_OIL, "030000ffb800ff00");
    TT_EQ(st.oil_c100, DECODE_TEMP_INVALID);
}

static void test_tank_reserve_bit(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_TANK, "0400800000000000");
    TT_EQ(st.tank_l, 0);
    TT_TRUE(st.tank_reserve);
}

static void test_accel(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_ACCEL, "7f00000000000000");
    TT_EQ(st.accel_mg, 0);                      /* 127 is the resting value */
    feed(&st, CAN_ID_ACCEL, "8900000000000000");
    TT_EQ(st.accel_mg, 100);                    /* 0.100 g */
}

/* --- the fuel counter, traps 3 and the masking -------------------------- */

static void test_counter_masking(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_FUEL, "f208ffff00000000");
    TT_EQ(st.fuel_counter, 0x7FFF);
    TT_TRUE(st.counter_wrapped);
    TT_TRUE(st.fuel_counter_valid);
}

static void test_counter_wrap_flag_clear(void)
{
    decode_state_t st;
    decode_init(&st);
    /* b3 = 0x7C, so bit 15 is zero -- this ignition cycle has not wrapped */
    feed(&st, CAN_ID_FUEL, "f2085c7c00000000");
    TT_EQ(st.fuel_counter, 0x7C5C);
    TT_FALSE(st.counter_wrapped);
}

static void test_counter_wrap_flag_set(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_FUEL, "f2085cfc00000000");
    TT_EQ(st.fuel_counter, 0x7C5C);
    TT_TRUE(st.counter_wrapped);
}

/* --- trap 1: the speed gate is a bit mask, not an equality -------------- */

static bool gate(uint8_t b1)
{
    decode_state_t st;
    uint8_t data[8] = { 0x00, 0x00, 0x5b, 0x13, 0xfe, 0xfe, 0x00, 0x13 };
    decode_init(&st);
    data[1] = b1;
    decode_frame(&st, CAN_ID_SPEED, data, 8);
    return st.speed_valid;
}

static void test_gate_accepted_states(void)
{
    TT_TRUE(gate(0x40));
    TT_TRUE(gate(0x48));        /* the majority state in 07_accel */
    TT_TRUE(gate(0x50));
    TT_TRUE(gate(0x58));
}

static void test_gate_rejected_states(void)
{
    TT_FALSE(gate(0x00));
    TT_FALSE(gate(0x42));       /* init ramp, two frames only */
    TT_FALSE(gate(0x43));       /* init ramp after ignition on */
    TT_FALSE(gate(0x03));
}

static void test_stale_speed_is_kept_but_flagged(void)
{
    decode_state_t st;
    decode_init(&st);
    feed(&st, CAN_ID_SPEED, "00405b13fefe0013");
    TT_TRUE(st.speed_valid);
    TT_EQ(st.speed_mmh, 24775);                 /* 24.775 km/h */

    /* The ramp must not overwrite the last good reading, only invalidate it. */
    feed(&st, CAN_ID_SPEED, "00430100fefe001d");
    TT_FALSE(st.speed_valid);
    TT_EQ(st.speed_mmh, 24775);
}

/* --- lengths ------------------------------------------------------------ */

static void test_short_frame_is_rejected(void)
{
    decode_state_t st;
    uint8_t data[8] = { 0 };
    decode_init(&st);
    /* DLC is not uniform on this bus: 0x050 carries 4 bytes and 0x5D0 six.
     * A decoder assuming 8 would read past the end of those. */
    TT_FALSE(decode_frame(&st, CAN_ID_ENGINE, data, 4));
    TT_FALSE(decode_frame(&st, CAN_ID_SPEED, data, 2));
    TT_TRUE(decode_frame(&st, CAN_ID_SPEED, data, 4));
}

static void test_unknown_id_is_ignored(void)
{
    decode_state_t st;
    uint8_t data[8] = { 0 };
    decode_init(&st);
    TT_FALSE(decode_frame(&st, 0x4A0, data, 8));
    TT_FALSE(decode_frame(&st, 0x488, data, 8));
}

/* --- against the real logs ---------------------------------------------- */

static void test_ign_only_is_engine_off_and_counter_zero(void)
{
    log_file_t lf;
    decode_state_t st;
    size_t i;
    uint16_t max_counter = 0;
    uint16_t max_rpm = 0;

    TT_TRUE(log_load("01_ign_only.txt", &lf, true));
    decode_init(&st);
    for (i = 0; i < lf.count; i++) {
        decode_frame(&st, lf.frames[i].can_id, lf.frames[i].data, lf.frames[i].dlc);
        if (st.fuel_counter > max_counter) { max_counter = st.fuel_counter; }
        if (st.rpm_q4 > max_rpm) { max_rpm = st.rpm_q4; }
    }
    TT_EQ(max_counter, 0);
    TT_EQ(max_rpm, 0);
    TT_EQ(st.clt_c100, 10050);      /* 100.5 C, per fixtures/README.md */
    log_free(&lf);
}

static void test_accel_peak_speed_needs_the_corrected_gate(void)
{
    log_file_t lf;
    decode_state_t st;
    size_t i;
    uint32_t peak = 0;

    TT_TRUE(log_load("07_accel.txt", &lf, true));
    decode_init(&st);
    for (i = 0; i < lf.count; i++) {
        decode_frame(&st, lf.frames[i].can_id, lf.frames[i].data, lf.frames[i].dlc);
        if (st.speed_valid && st.speed_mmh > peak) { peak = st.speed_mmh; }
    }
    /* 24.78 km/h, and it is only reachable because 0x48 passes the gate. */
    TT_EQ(peak, 24775);
    log_free(&lf);
}

static void test_idle_is_797_rpm(void)
{
    log_file_t lf;
    decode_state_t st;
    size_t i, n = 0;
    uint32_t sum = 0;

    TT_TRUE(log_load("02_idle_60s.txt", &lf, true));
    decode_init(&st);
    for (i = 0; i < lf.count; i++) {
        if (lf.frames[i].can_id != CAN_ID_ENGINE) { continue; }
        decode_frame(&st, lf.frames[i].can_id, lf.frames[i].data, lf.frames[i].dlc);
        sum += decode_rpm(&st);
        n++;
    }
    TT_TRUE(n > 1000);
    TT_NEAR(sum / n, 797, 3);
    log_free(&lf);
}

int main(void)
{
    printf("test_decode\n");
    TT_RUN(test_rpm);
    TT_RUN(test_torque_throttle_load);
    TT_RUN(test_clt);
    TT_RUN(test_clt_error_value);
    TT_RUN(test_oil_error_value);
    TT_RUN(test_tank_reserve_bit);
    TT_RUN(test_accel);
    TT_RUN(test_counter_masking);
    TT_RUN(test_counter_wrap_flag_clear);
    TT_RUN(test_counter_wrap_flag_set);
    TT_RUN(test_gate_accepted_states);
    TT_RUN(test_gate_rejected_states);
    TT_RUN(test_stale_speed_is_kept_but_flagged);
    TT_RUN(test_short_frame_is_rejected);
    TT_RUN(test_unknown_id_is_ignored);
    TT_RUN(test_ign_only_is_engine_off_and_counter_zero);
    TT_RUN(test_accel_peak_speed_needs_the_corrected_gate);
    TT_RUN(test_idle_is_797_rpm);
    return TT_SUMMARY();
}
