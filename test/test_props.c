/* test_props.c -- properties that hold for EVERY input, checked against
 * nothing but themselves.
 *
 * WHY THESE ARE SHAPED LIKE THIS. The rest of the suite compares the C core
 * against the Python reference over seventeen recordings. That is a strong
 * check and it has one blind spot, which cost the project a 6.4 % error in
 * every distance: the two implementations were written from the same table by
 * the same reasoning, so a mistake in the reasoning is a mistake in both, and
 * the diff stays clean. Twin implementations do not catch a fault they share.
 *
 * So nothing here consults an oracle. Each test states something that must be
 * true of the arithmetic itself -- a total is the sum of its parts, a value
 * stays inside the gauge that shows it, nothing changes when nothing happens --
 * and then tries to break it with inputs no fixture contains.
 *
 * ON FUZZING REACHABLE STATES ONLY. The generator below produces values the
 * bus can actually produce: a torque byte times TORQUE_CNM_PER_BIT rather than
 * an arbitrary uint16, a tank level masked to seven bits, a quarter-rpm count
 * that decode.c could really have written. Fuzzing beyond that manufactures
 * failures nobody can reach and teaches the reader to ignore the test.
 */

#include <string.h>

#include "compute.h"
#include "config.h"
#include "decode.h"
#include "txframes.h"
#include "tt.h"

/* xorshift32. Deterministic on purpose -- a test that fails once a fortnight
 * on a seed nobody recorded is worse than no test. */
static uint32_t rnd_state = 0x13579BDFu;

static uint32_t rnd(void)
{
    uint32_t x = rnd_state;
    x ^= x << 13;
    x ^= x >> 17;
    x ^= x << 5;
    rnd_state = x;
    return x;
}

static uint32_t rnd_upto(uint32_t n)
{
    return n == 0u ? 0u : rnd() % (n + 1u);
}

/* A bus state decode.c could have produced from real frames. */
static decode_state_t rnd_bus(void)
{
    decode_state_t st;
    decode_init(&st);
    st.rpm_q4 = (uint16_t)rnd_upto(7000u * 4u);
    st.torque_ind_cnm = (uint16_t)(rnd_upto(255u) * TORQUE_CNM_PER_BIT);
    st.throttle = (uint8_t)rnd_upto(255u);
    st.speed_valid = (rnd() & 1u) != 0u;
    st.speed_mmh = rnd_upto(300000u);           /* 300 km/h */
    st.tank_l = (uint8_t)rnd_upto(127u);        /* decode.c masks to seven bits */
    st.tank_valid = true;
    st.fuel_counter = (uint16_t)rnd_upto(COUNTER_MASK);
    st.fuel_counter_valid = true;
    return st;
}

/* Accumulators the core could have reached. The trip bounds are the caps from
 * config.h and not round numbers: past them compute_tick() resets, so a larger
 * value is not a state this core can be in -- and fuzzing states it cannot
 * reach is the habit this file's header argues against. */
static compute_t rnd_state_struct(void)
{
    compute_t c;
    uint8_t i;

    compute_init(&c);
    c.total_ul = rnd_upto(TRIP_MAX_UL);
    c.total_mm = rnd_upto(TRIP_MAX_MM);
    c.flow_ul_s = rnd_upto(5000u);
    c.tank_damped_ml = rnd_upto(127000u);
    c.tank_damped_valid = true;
    c.tank_rest_q8 = (uint16_t)rnd_upto(127u * 256u);
    c.tank_stable_l = (uint8_t)(c.tank_rest_q8 >> 8);
    c.tank_stable_valid = true;
    c.basis_q4 = (uint16_t)rnd_upto((uint32_t)FUELNOW_CLAMP_D << RANGE_BASIS_Q4);
    c.seg_cur_ul = rnd_upto(1000000u);
    c.seg_cur_mm = rnd_upto(RANGE_SEGMENT_MM - 1u);
    c.have_data = true;
    c.last_data_ms = 1000u;
    for (i = 0; i < (uint8_t)FLOW_BUCKETS; i++) {
        c.flow[i].ul = (uint16_t)rnd_upto(4000u);
        c.flow[i].ms = (uint16_t)rnd_upto(FLOW_BUCKET_MS);
    }
    return c;
}

/* ===================================================================== *
 *  Every getter, over ten thousand states no fixture contains.
 *
 *  Two things are under test and the first one is invisible in the source:
 *  a getter that divides by a value which can be zero does not return a
 *  wrong number on this machine, it raises SIGFPE and the test dies. Four
 *  of the getters divide by something derived from state. The second is
 *  the clamping the display depends on -- the TRI gauges behave
 *  unpredictably above their range, so FuelNow and FuelAvg must never
 *  leave 0..999 whatever the accumulators hold.
 * ===================================================================== */
static void test_no_state_can_break_a_getter(void)
{
    int i;
    for (i = 0; i < 10000; i++) {
        compute_t c = rnd_state_struct();
        decode_state_t st = rnd_bus();
        tx_values_t v;
        uint8_t f[TXFRAME_DLC];

        TT_TRUE(compute_fuel_now_d(&c, &st) <= FUELNOW_CLAMP_D);
        TT_TRUE(compute_avg_l100_d(&c) <= FUELNOW_CLAMP_D);
        (void)compute_flow_lh_c(&c);
        (void)compute_tank_d(&c);
        (void)compute_range_km(&c);
        (void)compute_trip_ml(&c);
        (void)compute_trip_m(&c);
        (void)compute_power_d(&st, compute_torque_d(&st));

        /* And the whole gather, which is what main.c actually calls. */
        txframes_gather(&v, &c, &st, 503, c.last_data_ms);
        txframes_fuel(&v, f);
        txframes_engine(&v, f);
        txframes_gather_trip(&v, &c, c.last_data_ms);
        txframes_trip(&v, f);
        TT_TRUE(v.fuel_now_d <= FUELNOW_CLAMP_D);
        TT_TRUE(v.fuel_avg_d <= FUELNOW_CLAMP_D);
    }
}

/* ===================================================================== *
 *  NO FRAME CAN BREAK THE DECODER.
 *
 *  decode.c guards every identifier with a length check -- `if (dlc < 4)
 *  return false` and its four siblings -- and until now those guards were
 *  believed rather than exercised: every fixture carries well-formed
 *  frames, because they were recorded off a working car. The bus is not
 *  obliged to be so polite. A transmission error inside the CAN CRC window
 *  is unlikely, but a frame from a module we have never seen, on an
 *  identifier that collides with one of ours, is not.
 *
 *  Two things are asserted. Nothing the decoder can be handed may put the
 *  state outside the range every consumer downstream assumes -- the tank
 *  masked to seven bits, the counter to fifteen -- and a frame too short
 *  for its identifier must change NOTHING, not merely return false.
 *
 *  DLC IS FUZZED 0..8 AND NOT BEYOND, deliberately. hal_can_receive() reads
 *  the length out of RXBnDLC and masks it to four bits, and the buffer it
 *  fills is eight bytes; a dlc above 8 is not something the hardware can
 *  hand to decode_frame(), so fuzzing it would test a caller that does not
 *  exist while the real bug -- reading data[7] on a two-byte frame -- is
 *  the one the guards are for.
 * ===================================================================== */
static void test_no_frame_can_break_the_decoder(void)
{
    static const uint16_t ours[] = { CAN_ID_SPEED, CAN_ID_ENGINE,
                                     CAN_ID_COOLANT, CAN_ID_TANK,
                                     CAN_ID_OIL, CAN_ID_FUEL };
    decode_state_t st;
    int i;

    decode_init(&st);
    for (i = 0; i < 50000; i++) {
        uint8_t data[8];
        uint16_t id;
        uint8_t dlc, b;

        for (b = 0; b < 8u; b++) {
            data[b] = (uint8_t)rnd();
        }
        /* Half the frames land on an identifier we accept, so the guards are
         * reached rather than skipped by the switch's default. */
        id = (rnd() & 1u) ? ours[rnd() % (sizeof ours / sizeof ours[0])]
                          : (uint16_t)(rnd() & 0x7FFu);
        dlc = (uint8_t)rnd_upto(8u);

        (void)decode_frame(&st, id, data, dlc);

        /* Invariants every consumer downstream relies on. tank_l indexes
         * nothing any more, but compute.c still shifts it into a q8 filter
         * and persist.c packs it into seven bits with the valid flag in the
         * eighth -- a 0xFF here would set that flag on a level of 127. */
        TT_TRUE(st.tank_l <= 0x7Fu);
        TT_TRUE(st.fuel_counter <= COUNTER_MASK);
        TT_TRUE(st.speed_mmh <= 65535u * 5u);
        TT_TRUE(st.torque_ind_cnm <= 255u * TORQUE_CNM_PER_BIT);
        TT_TRUE(st.clt_c100 == DECODE_TEMP_INVALID ||
                (st.clt_c100 >= -4800 && st.clt_c100 <= 14325));
        TT_TRUE(st.oil_c100 == DECODE_TEMP_INVALID ||
                (st.oil_c100 >= -4800 && st.oil_c100 <= 14325));
    }
}

/* A frame too short for its identifier must leave the state exactly as it
 * was. Returning false is not enough: decode.c reads data[7] for torque and
 * data[3] for the oil temperature, so a guard that returned false *after*
 * writing one field would pass every existing test and put a byte of
 * somebody else's frame on the display. */
static void test_a_short_frame_changes_nothing(void)
{
    static const struct { uint16_t id; uint8_t needs; } ids[] = {
        { CAN_ID_ENGINE,  8 }, { CAN_ID_SPEED,   4 },
        { CAN_ID_COOLANT, 2 }, { CAN_ID_OIL,     4 },
        { CAN_ID_TANK,    3 }, { CAN_ID_FUEL,    4 },
    };
    size_t k;
    uint8_t data[8];
    uint8_t b;

    for (b = 0; b < 8u; b++) {
        data[b] = 0xA5u;
    }

    for (k = 0; k < sizeof ids / sizeof ids[0]; k++) {
        decode_state_t st, before;
        uint8_t dlc;

        /* Start from a state that is not all zeroes, so a field quietly
         * cleared shows up as loudly as a field quietly set. */
        decode_init(&st);
        st.rpm_q4 = 3000u * 4u;
        st.torque_ind_cnm = 5000;
        st.throttle = 60;
        st.speed_mmh = 50000;
        st.speed_valid = true;
        st.tank_l = 40;
        st.tank_valid = true;
        st.clt_c100 = 9000;
        st.oil_c100 = 8000;
        st.fuel_counter = 1234;
        st.fuel_counter_valid = true;

        for (dlc = 0; dlc < ids[k].needs; dlc++) {
            before = st;
            TT_FALSE(decode_frame(&st, ids[k].id, data, dlc));
            TT_EQ(memcmp(&st, &before, sizeof st), 0);
        }
        /* And at the length it does need, it accepts -- or the loop above
         * would pass for a decoder that rejects everything. */
        TT_TRUE(decode_frame(&st, ids[k].id, data, ids[k].needs));
    }
}

/* A trip total is a sum of non-negative deltas, so it can only ever grow --
 * unless something cleared it, and then it must be exactly zero. There are
 * exactly two things allowed to do that, the refuelling rule and the runaway
 * cap in config.h, and the test knows about both by name. Anything else means
 * an accumulator moved for a reason nobody wrote down.
 *
 * The stream below stays far from the cap, so in practice only the first can
 * fire here; the cap is spelled out anyway, because an invariant that lists
 * its exceptions incompletely is how the next one gets missed. */
static void test_totals_only_move_forward(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    uint32_t prev_ul = 0, prev_mm = 0, prev_refuels = 0;
    uint16_t counter = 1234;
    int i;

    compute_init(&c);
    decode_init(&st);
    st.speed_valid = true;

    for (i = 0; i < 20000; i++) {
        /* A stream nothing in the fixtures resembles: the speed jumps about,
         * the engine stops and starts, the tank rises and falls, the frames
         * arrive at irregular intervals. */
        now += 1u + rnd_upto(60u);
        st.speed_mmh = rnd_upto(200000u);
        st.rpm_q4 = (uint16_t)((rnd_upto(20u) == 0u) ? 0u : rnd_upto(6000u * 4u));
        st.tank_l = (uint8_t)rnd_upto(60u);
        st.tank_valid = true;
        counter = (uint16_t)((counter + rnd_upto(200u)) % COUNTER_MODULO);
        st.fuel_counter = counter;
        st.fuel_counter_valid = true;

        compute_tick(&c, &st, now);
        compute_on_fuel(&c, &st, now);

        if (c.refuels != prev_refuels ||
            (prev_ul >= TRIP_MAX_UL || prev_mm >= TRIP_MAX_MM)) {
            /* The only event allowed to move a total downwards, and it must
             * take both of them to zero together. */
            TT_EQ(c.total_ul, 0);
            TT_EQ(c.total_mm, 0);
            TT_EQ(c.basis_q4, 0);
            prev_refuels = c.refuels;
        } else {
            TT_TRUE(c.total_ul >= prev_ul);
            TT_TRUE(c.total_mm >= prev_mm);
        }
        prev_ul = c.total_ul;
        prev_mm = c.total_mm;
    }
    /* The stream has to have exercised something, or the loop above proves
     * only that zero stays zero. */
    TT_TRUE(c.restarts > 0);
    TT_TRUE(prev_ul > 0);
}

/* The same frame twice is not twice the fuel. 0x480 has no fixed period and
 * the older fixtures are 39-51 % duplicates, so this is not a hypothetical --
 * it is the single most common malformation in the recordings. */
static void test_a_repeated_frame_adds_nothing(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t before;
    int i;

    compute_init(&c);
    decode_init(&st);
    st.rpm_q4 = 800u * 4u;
    st.fuel_counter_valid = true;

    st.fuel_counter = 5000;
    compute_on_fuel(&c, &st, 0);
    st.fuel_counter = 5100;
    compute_on_fuel(&c, &st, 40);
    before = c.total_ul;
    TT_EQ(before, 100);

    for (i = 0; i < 50; i++) {              /* the same reading, over and over */
        compute_on_fuel(&c, &st, (uint32_t)(41 + i));
    }
    TT_EQ(c.total_ul, before);
}

/* Distance is only ever integrated from a speed the car vouched for. An
 * invalid gate means the reading is the post-ignition ramp, which falls from
 * 464 to 0 and means nothing -- integrating it would invent metres. */
static void test_an_invalid_speed_never_invents_distance(void)
{
    compute_t c;
    decode_state_t st;
    uint32_t now = 0;
    int i;

    compute_init(&c);
    decode_init(&st);
    st.speed_valid = false;
    st.speed_mmh = 120000u;                 /* 120 km/h, and not to be believed */

    compute_tick(&c, &st, now);
    for (i = 0; i < 1000; i++) {
        now += 10u;
        compute_tick(&c, &st, now);
    }
    TT_EQ(c.total_mm, 0);

    /* And the moment the gate opens, the metres start where the car is, not
     * where it would have been. */
    st.speed_valid = true;
    for (i = 0; i < 100; i++) {
        now += 10u;
        compute_tick(&c, &st, now);
    }
    TT_NEAR(c.total_mm, 33333, 50);         /* 120 km/h for one second */
}

/* A freshly initialised core transmits zeros, not whatever the struct happened
 * to contain. compute_init memsets, so this is really a check that no getter
 * has a path that divides an empty accumulator by another empty one. */
static void test_an_empty_core_is_all_zeroes(void)
{
    compute_t c;
    decode_state_t st;
    tx_values_t v;

    compute_init(&c);
    decode_init(&st);
    txframes_gather(&v, &c, &st, 503, 0);
    txframes_gather_trip(&v, &c, 0);

    TT_EQ(v.fuel_now_d, 0);
    TT_EQ(v.fuel_avg_d, 0);
    TT_EQ(v.fuel_tank_d, 0);
    TT_EQ(v.range_km, 0);
    TT_EQ(v.power_d, 0);
    TT_EQ(v.torque_d, 0);
    TT_EQ(v.flow_c, 0);
    TT_EQ(v.trip_ml, 0);
    TT_EQ(v.trip_m, 0);
    TT_EQ(v.vdd_c, 503);                    /* ours, not the bus's */
}

int main(void)
{
    printf("test_props\n");
    TT_RUN(test_no_state_can_break_a_getter);
    TT_RUN(test_no_frame_can_break_the_decoder);
    TT_RUN(test_a_short_frame_changes_nothing);
    TT_RUN(test_totals_only_move_forward);
    TT_RUN(test_a_repeated_frame_adds_nothing);
    TT_RUN(test_an_invalid_speed_never_invents_distance);
    TT_RUN(test_an_empty_core_is_all_zeroes);
    return TT_SUMMARY();
}
