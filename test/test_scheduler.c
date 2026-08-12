/* test_scheduler.c -- the core driven the way main.c drives it, not the way
 * the other tests drive it.
 *
 * WHY THIS FILE EXISTS. Every other test here, and tools/replay.py with it,
 * feeds the core off the 0x480 frames: one compute_tick() per fuel frame,
 * ~38 ms apart. The firmware does not. It calls compute_tick() on every pass
 * of a scheduler that comes round every ~100 us, and on 2026-08-12 that
 * difference turned out to be hiding a 6.4 % under-reading of every distance
 * the device would have reported -- while the C and the Python agreed with
 * each other exactly, because they shared the fault.
 *
 * So the properties below are deliberately of a kind that CANNOT be checked
 * against the Python reference, because a shared oracle is exactly what let
 * that through:
 *
 *   - the answer must not depend on how often the core is called
 *   - total_ul must be the sum of the deltas, computed a second way
 *   - the EEPROM blindness must cost no fuel at all, which
 *     main.c asserts in a comment and nothing has ever tested
 *
 * sched.h is the harness. Only the timestamped fixtures can be used: a clock
 * synthesised from the frames would defeat the whole point.
 */

#include "compute.h"
#include "config.h"
#include "decode.h"
#include "sched.h"
#include "tt.h"

/* Six minutes of real driving with adapter timestamps -- the only fixture
 * long enough for the 1 s slot and the EEPROM interval to matter. */
#define DRIVE   "17_drive_property_z1.txt"

static sched_result_t run_opts(const char *log, sched_opts_t o)
{
    sched_result_t r;
    TT_TRUE(sched_run(log, o, &r));
    return r;
}

static sched_result_t run(const char *log, uint32_t tick_ms, bool eeprom)
{
    sched_opts_t o;
    o.tick_ms = tick_ms;
    o.jitter_ms = 0;
    o.eeprom_writes = eeprom;
    return run_opts(log, o);
}

/* ===================================================================== *
 *  THE PROPERTY THAT WOULD HAVE CAUGHT IT.
 *
 *  The core is offered the clock at 1 ms, at 10 ms and at 100 ms over the
 *  same recording. The fuel total is absolute, so it must come out
 *  IDENTICAL; the distance is integrated, so it may differ only by how
 *  finely the speed was sampled -- never by the millimetre the division
 *  used to throw away on every single call.
 *
 *  Before DIST_TICK_MS and the carried remainder, the 1 ms run reported
 *  about 6 % less distance than the 100 ms one on this fixture. Nothing in
 *  the suite could see it.
 * ===================================================================== */
static void test_answers_do_not_depend_on_the_tick_rate(void)
{
    sched_result_t fast = run(DRIVE, 1, false);
    sched_result_t mid  = run(DRIVE, 10, false);
    sched_result_t slow = run(DRIVE, 100, false);

    /* The counter is absolute: every pass reads the same 0x480 values in the
     * same order, so this is exact or something is wrong with the rule. */
    TT_EQ(mid.cp.total_ul, fast.cp.total_ul);
    TT_EQ(slow.cp.total_ul, fast.cp.total_ul);

    /* Distance: 0.5 % between the extremes. What is left is the sampling of
     * a changing speed -- a 100 ms step integrates the speed at the end of
     * the step over the whole step -- and NOT truncation, which is what the
     * carried remainder removed. */
    TT_TRUE(fast.cp.total_mm > 0);
    TT_NEAR(mid.cp.total_mm, fast.cp.total_mm, fast.cp.total_mm / 200u);
    TT_NEAR(slow.cp.total_mm, fast.cp.total_mm, fast.cp.total_mm / 200u);

    /* And the 1 ms run must not be the LOW one, which is the signature of the
     * fault: truncation always loses, so it can only ever bias downwards. */
    TT_TRUE(fast.cp.total_mm + fast.cp.total_mm / 500u >= mid.cp.total_mm);
}

/* The loop is not a timer, so neither is this. A pass of main.c takes between
 * 50 and 130 us depending on how many frames were waiting, and every hundredth
 * one carries the whole transmit slot -- an irregularity of a factor of thirty.
 * A property that holds on a regular grid and fails off it is not a property,
 * and an integrator that only works when its steps are equal is a bug waiting
 * for a busy bus. */
static void test_an_irregular_tick_changes_nothing(void)
{
    sched_opts_t o;
    sched_result_t even = run(DRIVE, 1, false);
    sched_result_t rough;

    o.tick_ms = 1;
    o.jitter_ms = 30;                   /* 1 to 31 ms between passes */
    o.eeprom_writes = false;
    rough = run_opts(DRIVE, o);

    TT_EQ(rough.cp.total_ul, even.cp.total_ul);
    TT_NEAR(rough.cp.total_mm, even.cp.total_mm, even.cp.total_mm / 200u);
    TT_EQ(rough.cp.refuels, even.cp.refuels);
}

/* total_ul computed a second way, from the same frames, by code that repeats
 * the restart rule but not the arithmetic. If compute_on_fuel ever counted a
 * delta twice, dropped one, or applied the modulo differently, this diverges
 * and no fixture number has to be updated to notice. */
static void test_the_total_is_the_sum_of_the_deltas(void)
{
    sched_result_t r = run(DRIVE, 1, false);
    TT_EQ(r.cp.refuels, 0);             /* or the total would have been cleared */
    TT_EQ(r.cp.total_ul, r.counter_sum_ul);
    TT_TRUE(r.cp.total_ul > 0);
}

/* ===================================================================== *
 *  main.c claims the EEPROM write is free, and until now
 *  that claim was a comment:
 *
 *    "the counter delta is (new - old) mod 32768, so a gap in the frames
 *     costs nothing at all; the next 0x480 accounts for everything burned
 *     during the write"
 *
 *  Here the write really does block for 48 ms and the frames that arrive
 *  behind it really are thrown away, exactly as the module would. The fuel
 *  total has to come out to the microlitre.
 * ===================================================================== */
static void test_eeprom_blindness_costs_no_fuel(void)
{
    sched_result_t quiet   = run(DRIVE, 1, false);
    sched_result_t writing = run(DRIVE, 1, true);

    /* The simulation has to have actually lost something, or this proves
     * nothing. Six minutes is five writes, ~17 frames each. */
    TT_TRUE(writing.frames_lost > 50);
    TT_TRUE(writing.frames_seen < quiet.frames_seen);

    /* And yet: not one microlitre. */
    TT_EQ(writing.cp.total_ul, quiet.cp.total_ul);

    /* Distance is integrated against the clock rather than against frame
     * arrivals, and the clock keeps running through the write, so it survives
     * too -- but the speed it integrates is 48 ms stale, so this one is a
     * tolerance rather than an equality. */
    TT_NEAR(writing.cp.total_mm, quiet.cp.total_mm, quiet.cp.total_mm / 200u);
}

/* The refuelling rule under the real scheduler, where the tank is sampled by
 * elapsed time rather than by frame arrival and the EEPROM write puts a 48 ms
 * hole in the samples. A false positive wipes an average the driver has
 * watched for 600 km.
 *
 * ONE LOG, not five. The sweep over all seventeen fixtures lives in
 * test_compute.c and is the broader check; what this adds is the driver, and
 * the driver does not become more convincing by being run five times. */
static void test_no_refuelling_under_the_scheduler(void)
{
    sched_result_t r = run(DRIVE, 1, true);
    TT_EQ(r.cp.refuels, 0);
}

/* Every value that reached a frame during six minutes of driving, checked
 * against the range its gauge can show. test_txframes.c does this for ONE
 * gather at the end of each log; this does it for all 3,600 of them, at the
 * rate the display really sees -- the harness carries the extremes so the
 * claim in the name is the claim the code makes. */
static void test_every_gather_stays_inside_the_gauges(void)
{
    sched_result_t r = run(DRIVE, 10, false);

    TT_TRUE(r.gathers > 3000);
    TT_TRUE(r.max_fuel_now_d <= FUELNOW_CLAMP_D);
    TT_TRUE(r.max_fuel_avg_d <= FUELNOW_CLAMP_D);
    /* Range is a uint16 on the wire and the tank is under 60 l, so anything
     * above a few thousand kilometres means the basis collapsed towards zero
     * rather than that the car became efficient. */
    TT_TRUE(r.max_range_km < 3000u);
    /* And the extremes were actually reached, or the three lines above are
     * checking that zero is small. */
    TT_TRUE(r.max_fuel_now_d > 0);
    TT_TRUE(r.max_range_km > 0);
}

/* A pass that does nothing must change nothing. main.c calls compute_tick()
 * thousands of times a second and the overwhelming majority of those calls
 * have to be pure no-ops -- if one of them moved an accumulator by a bit, the
 * error would scale with the loop rate rather than with the car. */
static void test_a_pass_with_no_time_in_it_changes_nothing(void)
{
    compute_t a, b;
    decode_state_t st;
    uint32_t now = 100000;
    int i;

    compute_init(&a);
    decode_init(&st);
    st.speed_valid = true;
    st.speed_mmh = 50000;
    st.tank_l = 30;

    compute_tick(&a, &st, now);         /* the first call only starts the clock */
    now += 1000;
    compute_tick(&a, &st, now);         /* and this one does the work */

    b = a;
    for (i = 0; i < 100; i++) {
        compute_tick(&b, &st, now);     /* same millisecond, a hundred times */
    }
    TT_EQ(memcmp(&a, &b, sizeof a), 0);
}

int main(void)
{
    printf("test_scheduler\n");
    TT_RUN(test_answers_do_not_depend_on_the_tick_rate);
    TT_RUN(test_an_irregular_tick_changes_nothing);
    TT_RUN(test_the_total_is_the_sum_of_the_deltas);
    TT_RUN(test_eeprom_blindness_costs_no_fuel);
    TT_RUN(test_no_refuelling_under_the_scheduler);
    TT_RUN(test_every_gather_stays_inside_the_gauges);
    TT_RUN(test_a_pass_with_no_time_in_it_changes_nothing);
    return TT_SUMMARY();
}
