/* compute.c -- see compute.h. PURE C, no hardware.
 *
 * The traps this file exists to avoid are written up in docs/firmware/can-decoding.md.
 * Three of the four live in here: the restart rule, the modulo delta and the
 * minimum distance under the average.
 */

#include <string.h>

#include "compute.h"
#include "divconst.h"

/* --- helpers ------------------------------------------------------------ */

/* Where the start detector is. The order is not meaningful. */
#define HEALTH_START_UNKNOWN    0u      /* since power-up, no 0x280 yet        */
#define HEALTH_START_STOPPED    1u      /* engine speed zero                   */
#define HEALTH_START_CRANKING   2u      /* turning, not yet START_FIRED_RPM    */
#define HEALTH_START_DIPWIN     3u      /* fired, watching the fall-back       */
#define HEALTH_START_RUNNING    4u      /* measured, or never seen from rest   */

static uint32_t elapsed(uint32_t now, uint32_t then)
{
    /* The millisecond clock is free running and wraps after 49 days. Unsigned
     * subtraction gives the right answer across the wrap, which a signed
     * comparison would not. */
    return now - then;
}

static uint32_t div_round(uint32_t num, uint32_t den)
{
    return den == 0u ? 0u : (num + den / 2u) / den;
}

static uint16_t clamp_u16(uint32_t v, uint32_t limit)
{
    return (uint16_t)(v > limit ? limit : v);
}

/* --- the flow window ---------------------------------------------------- */

static void flow_clear(compute_t *c)
{
    memset(c->flow, 0, sizeof c->flow);
    c->flow_open = 0;
    c->flow_ul_s = 0;
}

/* ! HOT PATH. Runs on every 0x480, which is ~26 times a second. Read
 * ! docs/firmware/optimisation.md before adding anything to it -- especially a
 * ! division, which costs 1,026 cycles on this part.
 *
 * A frame adds to the open bucket and nothing else. When that bucket has held
 * FLOW_BUCKET_MS it closes, the four buckets are averaged, and the oldest is
 * emptied to become the new open one -- so the division happens four times a
 * second rather than twenty-six, and the window is always a whole number of
 * buckets rather than a queue to be trimmed one sample at a time.
 *
 * The previous shape, a 32-slot ring with a drop loop, is described in
 * config.h next to FLOW_BUCKET_MS along with what this trades for it. */
static void flow_push(compute_t *c, uint16_t ul, uint16_t ms)
{
    flow_bucket_t *open = &c->flow[c->flow_open];
    uint32_t sum_ul = 0;
    uint16_t sum_ms = 0;
    uint8_t i;

    open->ul = (uint16_t)(open->ul + ul);
    open->ms = (uint16_t)(open->ms + ms);

    if (open->ms < (uint16_t)FLOW_BUCKET_MS) {
        return;                 /* still filling, and that is the whole cost */
    }

    for (i = 0; i < (uint8_t)FLOW_BUCKETS; i++) {
        sum_ul += c->flow[i].ul;
        sum_ms = (uint16_t)(sum_ms + c->flow[i].ms);
    }
    c->flow_ul_s = div_round(mul_u32_u16(sum_ul, 1000u), sum_ms);

    /* Compare rather than a modulo, as everywhere else here. The bucket we
     * move to is the oldest of the four and has to be emptied to become the
     * new open one. */
    if (++c->flow_open >= (uint8_t)FLOW_BUCKETS) {
        c->flow_open = 0;
    }
    c->flow[c->flow_open].ul = 0;
    c->flow[c->flow_open].ms = 0;
}

/* --- the rolling basis behind Range -------------------------------------- */

/* One completed kilometre folded into the basis. Called from compute_tick, so
 * at most once per 10 ms step and in practice once every 45 seconds of
 * motorway driving -- there is nothing hot about this path.
 *
 * ONE MICROLITRE PER METRE IS EXACTLY 0.1 l/100 km, and a segment is exactly
 * one kilometre, so the whole conversion is a division by 1000 -- and 1000 is
 * one of the divisors with a free shift in divconst.h.
 *
 * THERE IS NO SEEDING CASE HERE ANY MORE, AND ITS ABSENCE IS THE POINT.
 * This used to open with `if (basis_q4 == 0) { basis_q4 = km_q4; return; }` --
 * one kilometre became the whole estimate, undamped. Every consumer of that
 * branch was a moment when the basis had just been zeroed: an ignition cycle
 * (basis_q4 did not reach the EEPROM, total_mm did) or a refuelling. Both put
 * the car at a filling station, so the kilometre that seeded the number was
 * the worst kilometre available -- forecourt manoeuvring, a cold-ish engine,
 * and minutes of idling whose microlitres all land in one segment because
 * seg_cur_ul grows while the car stands still and seg_cur_mm does not.
 * Measured, not assumed: 17_drive_property_z1 is 880 m of exactly that and
 * runs at 23.2 l/100 km, against 11-ish on the road. Range therefore halved
 * on leaving a filling station and crawled back over the next fifty
 * kilometres at one time constant of sixteen. config.h has the numbers.
 *
 * The basis is never zero now -- compute_init, compute_restore and
 * compute_reset_trip between them guarantee it -- so every kilometre goes
 * through the filter below and no single one can move the estimate by more
 * than a sixteenth. A kilometre that burned nothing at all, possible on a
 * long descent where the ECU cuts the injectors, is one such kilometre and
 * needs no special case either. */
static void range_basis_update(compute_t *c)
{
    uint16_t km_q4 = (uint16_t)(clamp_u16(div_const(c->seg_cur_ul, DIVC_1000),
                                          FUELNOW_CLAMP_D) << RANGE_BASIS_Q4);

    if (km_q4 > c->basis_q4) {
        c->basis_q4 = (uint16_t)(c->basis_q4 +
                      ((km_q4 - c->basis_q4) >> RANGE_BASIS_SHIFT));
    } else {
        c->basis_q4 = (uint16_t)(c->basis_q4 -
                      ((c->basis_q4 - km_q4) >> RANGE_BASIS_SHIFT));
    }
}

/* --- the tank, and the refuelling trigger -------------------------------- */

/* The settled level: first order over the at-rest samples, in 1/256 l so the
 * step is a shift and not a division. TANK_REST_SHIFT is the time constant in
 * samples, i.e. in seconds. Pulled out of tank_sample() so the settling
 * window and the armed path can share it without either drifting. */
static void tank_rest_filter(compute_t *c, uint16_t target_q8)
{
    if (target_q8 > c->tank_rest_q8) {
        c->tank_rest_q8 = (uint16_t)(c->tank_rest_q8 +
                          ((target_q8 - c->tank_rest_q8) >> TANK_REST_SHIFT));
    } else {
        c->tank_rest_q8 = (uint16_t)(c->tank_rest_q8 -
                          ((c->tank_rest_q8 - target_q8) >> TANK_REST_SHIFT));
    }
    c->tank_stable_l = (uint8_t)(c->tank_rest_q8 >> 8);
}

static void tank_sample(compute_t *c, const decode_state_t *st)
{
    uint32_t target_ml;
    uint16_t target_q8;

    /* Nothing has told us the level yet, so there is nothing to sample. A
     * zero here is not a reading, it is decode_init(), and the difference
     * cannot be recovered later: the first at-rest sample LATCHES the
     * baseline the refuelling rule compares against for the rest of the
     * trip, and persist.c writes it to the EEPROM. On a bench with no 0x320
     * on the bus that fabricated "0 litres, trustworthy" survives the power
     * cycle and then reads a normal tank as a refuelling. In the car 0x320 is
     * periodic and arrives long before the first sample, so this gate never
     * fires there -- which is exactly why nothing on the car would have
     * caught it. */
    if (!st->tank_valid) {
        return;
    }

    target_ml = mul_u32_u16(st->tank_l, 1000u);

    /* The displayed level is damped whether we are moving or not -- that is
     * what the damping is for. First order, one sample a second, so the time
     * constant is TANK_DAMP_SAMPLES seconds. */
    if (!c->tank_damped_valid) {
        c->tank_damped_ml = target_ml;
        c->tank_damped_valid = true;
    } else if (target_ml > c->tank_damped_ml) {
        c->tank_damped_ml += (target_ml - c->tank_damped_ml) >> TANK_DAMP_SHIFT;
    } else {
        c->tank_damped_ml -= (c->tank_damped_ml - target_ml) >> TANK_DAMP_SHIFT;
    }

    /* The baseline the refuelling rule watches is only fed while standing.
     * While driving the float sloshes over a 9-10 L spread on every corner,
     * so the reading is worthless; at rest one litre dominates completely --
     * 1584 of 1622 measured samples were the same litre.
     * docs/firmware/refuel-reset.md has the measurement.
     *
     * THAT MEASUREMENT WAS TAKEN ON A CAR THAT HAD BEEN STANDING, which is
     * not the same claim as "a car whose speed has just reached zero", and
     * the difference is the settling window below. */
    if (st->speed_mmh >= TANK_STATIONARY_MMH) {
        c->rest_s = 0;
        c->refuel_high = 0;
        c->have_moved = true;
        return;
    }

    target_q8 = (uint16_t)((uint16_t)st->tank_l << 8);

    if (!c->tank_stable_valid) {
        /* First at-rest reading ever, or the first after an empty EEPROM.
         * Initialise only -- resetting here would clear the average every
         * time the device is powered up. */
        c->tank_rest_q8 = target_q8;
        c->tank_stable_l = st->tank_l;
        c->tank_stable_valid = true;
        return;
    }

    /* THE FLOAT IS STILL MOVING FOR THE FIRST REFUEL_ARM_S OF ANY STOP, so
     * the rule is not armed yet. config.h has what that cost: the raw level
     * spans five litres on a fully stopped car in a log of repeated short
     * stops, and only the consecutive-sample counter stood between that and a
     * cleared trip.
     *
     * WHAT HAPPENS TO THE REFERENCE IN THAT WINDOW IS THE WHOLE DESIGN, and
     * the two cases want opposite things:
     *
     *   ARRIVED HERE (have_moved). The filter runs, so the reference takes up
     *   whatever the level reads at this spot -- including a tilt, which is
     *   what stops a car parked on a slope reading as a refuelling. The rule
     *   then arms against the level HERE, so only a rise that happens while
     *   we are parked can fire it. Absorbing a genuine fill this way needs
     *   somebody to stop, get out, open the cap and be pumping inside twenty
     *   seconds.
     *
     *   STARTED HERE (!have_moved). The filter is frozen and the EEPROM
     *   reference stands, because a refuelling with the ignition off leaves
     *   no arrival to observe and that stored figure is the only record of
     *   what the tank held beforehand. Chasing the level here would lose the
     *   ordinary way of refuelling altogether.
     *
     * ⚠ The price of the second case is in config.h and it is not a tuning
     * problem: parked on a slope and key-cycled is indistinguishable from
     * fuel added while parked, and this firmware resolves it in favour of
     * detecting the fill. */
    if (c->rest_s < (uint8_t)REFUEL_ARM_S) {
        c->rest_s++;
        if (c->have_moved) {
            tank_rest_filter(c, target_q8);
        }
        return;
    }

    /* Persistently higher than the settled level means somebody refuelled.
     *
     * THE BASELINE IS FROZEN WHILE THE COUNTER RUNS, and that is the whole
     * trick: if the filter below were allowed to chase the new level it would
     * raise tank_stable_l under the comparison and disqualify the very rise it
     * is in the middle of confirming -- a 4 l fill would be detected or not
     * depending on how fast the filter happened to move. Held still, the rule
     * is exactly what it says: REFUEL_CONFIRM_S consecutive at-rest samples
     * more than REFUEL_RISE_L above the settled level.
     *
     * The subtraction cannot underflow: the > guards it. */
    if (st->tank_l > c->tank_stable_l &&
        (uint8_t)(st->tank_l - c->tank_stable_l) > REFUEL_RISE_L) {
        if (++c->refuel_high >= (uint8_t)REFUEL_CONFIRM_S) {
            compute_reset_trip(c);
            c->refuels++;
            c->refuel_high = 0;
            /* Snap everything to the new level rather than letting the filters
             * crawl up to it. A refuelling is the one change in tank level
             * that is both large and instantaneous, and it is the one moment
             * the driver is certain to look at the gauge. Without this the
             * level and the range would both read minutes-old for minutes
             * after filling up. */
            c->tank_rest_q8 = target_q8;
            c->tank_stable_l = st->tank_l;
            c->tank_damped_ml = mul_u32_u16(st->tank_l, 1000u);
        }
        return;
    }
    c->refuel_high = 0;

    tank_rest_filter(c, target_q8);
}

/* --- lifecycle ---------------------------------------------------------- */

void compute_init(compute_t *c)
{
    memset(c, 0, sizeof *c);
    /* A device that has never driven a kilometre still has to divide by
     * something, and the conservative default is that something. Starting the
     * filter here rather than at zero is what removes the undamped seeding
     * case from range_basis_update() -- see the comment there. */
    c->basis_q4 = (uint16_t)(RANGE_DEFAULT_L100_D << RANGE_BASIS_Q4);

    /* Nothing is known about the start until the engine has been seen
     * stopped: a converter that wakes with the crank already turning must not
     * publish a crank time it started timing late. */
    c->health.start_phase = HEALTH_START_UNKNOWN;
    c->health.start_crank = HEALTH_UNKNOWN;
    c->health.start_dip   = HEALTH_UNKNOWN;
    c->health.start_clt   = HEALTH_UNKNOWN;
}

void compute_reset_trip(compute_t *c)
{
    c->total_ul = 0;
    c->total_mm = 0;
    c->seg_cur_ul = 0;
    c->seg_cur_mm = 0;
    /* THE BASIS DELIBERATELY SURVIVES THIS, and it used to be zeroed here.
     * The old reasoning was that the basis is a property of the trip that was
     * just discarded. It is not: the trip counter is a property of the
     * counter, the rolling basis is a property of how the car is being
     * driven, and filling the tank changes the first and nothing at all about
     * the second. The same car with the same driver on the same road burns
     * the same fuel a minute after a refuelling as it did a minute before.
     *
     * Zeroing it here is half of the fault described in range_basis_update():
     * it handed the next kilometre -- the one pulling off a forecourt -- the
     * whole estimate. The other half was the ignition cycle, and
     * compute_restore() closes that one. */
}

void compute_restore(compute_t *c, uint32_t total_ul, uint32_t total_mm,
                     uint8_t tank_stable_l, bool tank_stable_valid)
{
    c->total_ul = total_ul;
    c->total_mm = total_mm;
    c->tank_stable_l = tank_stable_l;
    c->tank_stable_valid = tank_stable_valid;
    /* Seed the filter from what came out of the EEPROM rather than from the
     * first sample after the restart. Seeding it from the sample would let a
     * single reading move the baseline by however much the tank had changed
     * while the ignition was off -- which is precisely the change the
     * refuelling rule exists to notice. */
    c->tank_rest_q8 = (uint16_t)((uint16_t)tank_stable_l << 8);

    /* AND THE RANGE FILTER GETS THE SAME TREATMENT, for the same reason and
     * one line lower. It did not, and that was the other half of the fault in
     * range_basis_update(): the record carries the totals but not basis_q4,
     * so every ignition cycle restored a large total_mm beside a basis of
     * zero, and the first kilometre after the key turn became the whole
     * estimate.
     *
     * THE SEED IS THE TRIP AVERAGE, WHICH COSTS NOTHING TO STORE BECAUSE IT
     * IS ALREADY STORED. total_ul over total_mm is this car's own consumption
     * over everything since the last fill-up -- a far better opening guess
     * than RANGE_DEFAULT_L100_D and a far better one than any single
     * kilometre. Adding basis_q4 to persist_record_t would be the obvious
     * alternative and it is not worth a byte of EEPROM: the record is packed
     * to twelve with a full CRC-16, a thirteenth byte drops the ring from 64
     * slots to 59, and the number it would store is one the ring can already
     * reconstruct.
     *
     * RANGE_MIN_MM and not AVG_MIN_MM: below five kilometres the ratio is a
     * handful of city blocks and the conservative default is the better
     * guess. compute_avg_l100_d() clamps to FUELNOW_CLAMP_D, so the shift
     * cannot overflow the uint16; it returns zero below AVG_MIN_MM, which
     * RANGE_MIN_MM already excludes, and the test costs one compare against
     * the alternative of dividing by it. */
    if (c->total_mm >= RANGE_MIN_MM) {
        uint16_t avg_d = compute_avg_l100_d(c);
        if (avg_d > 0u) {
            c->basis_q4 = (uint16_t)(avg_d << RANGE_BASIS_Q4);
        }
    }
}

/* --- the fuel counter --------------------------------------------------- */

void compute_on_fuel(compute_t *c, const decode_state_t *st, uint32_t now_ms)
{
    uint16_t delta_ul;
    uint32_t dt_ms;

    if (!st->fuel_counter_valid) {
        return;
    }

    c->last_data_ms = now_ms;
    c->have_data = true;

    /* Trap 2. The counter drops to zero when the ignition goes off, so the
     * next delta would be tens of thousands of microlitres out of nowhere.
     * The engine also has to be turning for a delta to mean anything. */
    if (st->fuel_counter == 0u || st->rpm_q4 == 0u) {
        if (c->have_prev) {
            c->restarts++;
        }
        c->prev_counter = st->fuel_counter;
        c->last_fuel_ms = now_ms;
        c->have_prev = true;
        /* Unlike the Python reference we also drop the window here, so the
         * flow reads zero with the engine stopped instead of freezing at
         * whatever was burning when it was switched off. */
        flow_clear(c);
        return;
    }

    if (!c->have_prev) {
        c->prev_counter = st->fuel_counter;
        c->last_fuel_ms = now_ms;
        c->have_prev = true;
        return;
    }

    /* Fifteen bits, so the difference is taken modulo 32768. Bit 15 has
     * already been masked off in decode.c -- it is a wrap flag, not data. */
    delta_ul = (uint16_t)((st->fuel_counter - c->prev_counter) % COUNTER_MODULO);
    c->prev_counter = st->fuel_counter;

    dt_ms = elapsed(now_ms, c->last_fuel_ms);
    c->last_fuel_ms = now_ms;

    c->total_ul += delta_ul;
    c->seg_cur_ul += delta_ul;

    if (dt_ms > 0u && dt_ms <= (uint32_t)FLOW_WINDOW_MS) {
        flow_push(c, delta_ul, (uint16_t)dt_ms);
    } else if (dt_ms > (uint32_t)FLOW_WINDOW_MS) {
        /* A gap longer than the whole window. Whatever the buckets held
         * describes a different situation entirely -- and the bus is declared
         * dead at half this, so the display is already showing zeros. The
         * bound is also what keeps a bucket inside its uint16 fields. */
        flow_clear(c);
    }
}

/* --- distance and the periodic sampling --------------------------------- */

void compute_tick(compute_t *c, const decode_state_t *st, uint32_t now_ms)
{
    uint32_t dt_ms;

    if (!c->have_tick) {
        c->have_tick = true;
        c->last_tick_ms = now_ms;
        c->last_tank_ms = now_ms;
        return;
    }

    /* DIST_TICK_MS AND NOT EVERY CALL, and config.h argues that at length: on
     * the real part a pass is 113 us, so integrating on every one of them
     * means a delta of one millisecond, and a millisecond of distance
     * truncated to whole millimetres loses several per cent of the trip --
     * everything, below 3.6 km/h. Time that has not been integrated yet stays
     * in last_tick_ms, so nothing is lost by waiting for the step. */
    dt_ms = elapsed(now_ms, c->last_tick_ms);
    if (dt_ms >= (uint32_t)DIST_TICK_MS) {
        c->last_tick_ms = now_ms;

        /* v [0.001 km/h] * t [ms] / 3600 = s [mm]. A gap longer than a second
         * means we were not watching, and guessing across it would invent
         * distance the car may never have covered.
         *
         * DIST_MIN_MMH and not > 0: a standing car sends 0.005 km/h, not
         * zero, and with the remainder carried below that would creep 83 mm
         * per minute of idling. config.h has the measurement. */
        if (st->speed_valid && st->speed_mmh > (uint32_t)DIST_MIN_MMH &&
            dt_ms <= 1000u) {
            /* The remainder of the division is carried into the next step
             * rather than discarded, which is what makes the integration
             * exact instead of biased low by up to one millimetre per step.
             * It is under 3600 by construction -- under one millimetre of
             * distance -- so one left behind by the gap above is meaningless
             * and is deliberately not cleared.
             *
             * dt_ms is gated to 1000 by the condition above, so it fits the
             * uint16 mul_u32_u16 takes -- which is why that gate is
             * load-bearing for more than just the distance it guards. */
            uint32_t num = mul_u32_u16(st->speed_mmh, (uint16_t)dt_ms)
                         + c->dist_rem;
            uint32_t mm = div_const(num, DIVC_3600);

            c->dist_rem = (uint16_t)(num - mul_u32_u16(mm, 3600u));
            c->total_mm += mm;
            c->seg_cur_mm += mm;

            while (c->seg_cur_mm >= RANGE_SEGMENT_MM) {
                range_basis_update(c);
                c->seg_cur_ul = 0;
                c->seg_cur_mm -= RANGE_SEGMENT_MM;
            }
        }
    }

    if (elapsed(now_ms, c->last_tank_ms) >= TANK_SAMPLE_MS) {
        c->last_tank_ms = now_ms;
        tank_sample(c, st);
    }

    /* The last line of defence, and it is checked here rather than where the
     * accumulators grow so that there is exactly one of it. Nothing else ever
     * clears them but a detected refuelling, and total_mm wraps at 4,295 km --
     * config.h argues the caps and why this resets rather than saturates.
     * Two 32-bit compares a hundred times a second; it costs nothing and it
     * is the only thing standing between a failed tank sender and a trip
     * meter that silently starts counting again from zero. */
    if (c->total_mm >= TRIP_MAX_MM || c->total_ul >= TRIP_MAX_UL) {
        compute_reset_trip(c);
    }
}

bool compute_data_live(const compute_t *c, uint32_t now_ms)
{
    return c->have_data && elapsed(now_ms, c->last_data_ms) <= DATA_TIMEOUT_MS;
}

/* --- derived quantities -------------------------------------------------- */

uint16_t compute_flow_lh_c(const compute_t *c)
{
    /* l/h = ul/s * 3.6 / 1000, so in 0.01 l/h it is ul/s * 0.36. */
    return clamp_u16(div_const_round(mul_u32_u16(c->flow_ul_s, 36u), 50u,
                                     DIVC_100), 0xFFFFu);
}

uint16_t compute_fuel_now_d(const compute_t *c, const decode_state_t *st)
{
    /* Dual unit, a single threshold and no hysteresis: the jump when it
     * switches is the visual cue that it switched. Without a trustworthy
     * speed, l/100 km is meaningless, so l/h is sent. */
    if (!st->speed_valid || st->speed_mmh < FUELNOW_LH_BELOW_MMH) {
        /* l/h at 0.1 = ul/s * 3.6 / 100 */
        return clamp_u16(div_const_round(mul_u32_u16(c->flow_ul_s, 36u), 500u,
                                         DIVC_1000), FUELNOW_CLAMP_D);
    }
    /* l/100 km at 0.1 = ul/s * 3600 / v[0.001 km/h] */
    return clamp_u16(div_round(mul_u32_u16(c->flow_ul_s, 3600u), st->speed_mmh),
                     FUELNOW_CLAMP_D);
}

uint16_t compute_avg_l100_d(const compute_t *c)
{
    /* Trap 4. Right after starting, distance is nearly zero and the ratio
     * runs away -- on 06_trip_reset it gave 21,395 l/100 km before the car
     * had moved at all. */
    if (c->total_mm < AVG_MIN_MM) {
        return 0;
    }
    /* One microlitre per metre is exactly 0.1 l/100 km, which is the unit the
     * frame wants, so the whole conversion is one division. */
    return clamp_u16(div_round(c->total_ul, div_const(c->total_mm, DIVC_1000)),
                     FUELNOW_CLAMP_D);
}

uint16_t compute_tank_d(const compute_t *c)
{
    return clamp_u16(div_const_round(c->tank_damped_ml, 50u, DIVC_100), 0xFFFFu);
}

uint16_t compute_range_km(const compute_t *c)
{
    /* THERE IS NO DISTANCE GATE HERE ANY MORE. It used to read
     * `if (total_mm >= RANGE_MIN_MM && basis_q4 > 0)`, falling back to the
     * default otherwise, and both halves have gone for the same reason: the
     * basis now always holds a usable number. It starts at the default in
     * compute_init(), is seeded from the persisted trip average in
     * compute_restore(), survives compute_reset_trip(), and moves by at most
     * a sixteenth per kilometre after that. The gate also produced a step --
     * Range jumped the instant the trip crossed five kilometres, from the
     * default to whatever the first few kilometres had built -- which is the
     * jumping this whole filter exists to avoid.
     *
     * The floor below is not the old gate in disguise and it must stay. With
     * RANGE_BASIS_SHIFT = 4 a difference under sixteen shifts to zero, so a
     * basis below 1.0 l/100 km cannot walk down any further but can sit at
     * 15/16 of a tenth, which truncates to zero tenths. Reachable only on a
     * kilometre that burned nothing -- and reachable is the whole test:
     * test_props.c fuzzes every getter precisely because a division by a
     * reachable zero here is SIGFPE, not a wrong number. */
    uint32_t basis_d = (uint32_t)(c->basis_q4 >> RANGE_BASIS_Q4);

    if (basis_d == 0u) {
        basis_d = RANGE_DEFAULT_L100_D;
    }

    /* THE DAMPED LEVEL, NOT THE INSTANTANEOUS ONE. Reading
     * st->tank_l, which is the raw float position and slosh and all: on
     * 07_accel the raw value swings over 10 L during a pull-away, which is
     * 111 km of range appearing and disappearing several times a second while
     * the level shown right next to it sat still. The damping that
     * compute_tank_d already had is worth exactly as much here, and the two
     * gauges have no business disagreeing about how much fuel is in the tank.
     *
     * The settled level would be steadier still, but it only updates at rest,
     * so it would leave the range frozen for a whole motorway drive. The
     * damped value tracks consumption; that is the point of it.
     *
     * km = litres / (l/100 km) * 100, and basis is in tenths. Litres here are
     * millilitres, so the 1000 of the old line is gone. */
    return clamp_u16(c->tank_damped_ml / basis_d, 0xFFFFu);
}

uint32_t compute_trip_ml(const compute_t *c)
{
    return div_const(c->total_ul, DIVC_1000);
}

uint32_t compute_trip_m(const compute_t *c)
{
    return div_const(c->total_mm, DIVC_1000);
}

uint16_t compute_torque_d(const decode_state_t *st)
{
    /* Drag torque -- friction, pumping, alternator -- is not constant; it
     * rises with engine speed and is modelled linearly. The four calibration
     * points come out of the warm free-revving holds, see config.h. */
    uint32_t rpm = decode_rpm(st);
    uint32_t drag_cnm;
    uint32_t net_cnm;

    /* Cranking is not running, and b7 is not torque while the starter turns
     * the engine -- see TORQUE_MIN_RPM. This also covers the engine being off,
     * where rpm is zero. */
    if (rpm < TORQUE_MIN_RPM) {
        return 0;
    }

    /* TORQUE AND POWER ARE SHOWN ONLY WHILE THE CAR IS MOVING AND THE DRIVER
     * IS ASKING FOR TORQUE. THIS RULE IS FIXED AND IS NOT TO BE RELAXED,
     * WHATEVER A FUTURE DRAG REFIT SAYS.
     *
     * IT IS AN OR AND NOT AN AND, and the difference is two states the car is
     * not in: revving in neutral at a standstill, and the last few seconds of
     * every roll to a stop, where the idle governor lifts b7 back above the
     * drag line while the pedal never moves. Both are the same fault -- the
     * drag line is systematically low at idle, because no straight line in rpm
     * passes through both idle and the free-revving holds -- so idle is
     * asserted here rather than fitted, for every state the engine idles in.
     * config.h holds the two thresholds, the measurement behind each, the
     * worked stop, and what the rule costs on a pull-away. */
    if (st->speed_mmh <= STANDSTILL_MMH || st->throttle <= THROTTLE_REST) {
        return 0;
    }

    /* A shift of 16 is three byte moves and no loop at all, which is why the
     * slope is scaled by 2**16 rather than by 10,000. rpm is under 16384, so
     * the product cannot leave 32 bits. */
    drag_cnm = (uint32_t)DRAG_TORQUE_BASE_CNM +
               (mul_u32_u16(rpm, (uint16_t)DRAG_TORQUE_SLOPE_Q16) >> 16);

    if (st->torque_ind_cnm <= drag_cnm) {
        return 0;               /* on the overrun the engine is being driven */
    }
    net_cnm = st->torque_ind_cnm - drag_cnm;

    /* The owner's own gain, zero unless somebody set it -- config.h argues
     * why it exists and why it is a fixed constant rather than a live
     * correction factor. It goes on NET torque, where a dynamometer measures,
     * and power inherits it because compute_power_d() is handed this result.
     * It is applied before the division to tenths so the trim keeps the
     * hundredth the drag subtraction was carried in. */
    net_cnm = compute_trim_apply(net_cnm, TORQUE_TRIM_Q8);

    return clamp_u16(div_const_round(net_cnm, 5u, DIVC_10), 0xFFFFu);
}

uint32_t compute_trim_apply(uint32_t value, int16_t trim_q8)
{
    uint32_t delta;

    /* The default is one comparison and a return, so a build nobody has
     * trimmed pays essentially nothing for the feature existing. */
    if (trim_q8 == 0) {
        return value;
    }

    if (trim_q8 > 0) {
        /* value is a net torque in 0.01 Nm, so at the full scale b7 can reach
         * it is under 26,100; times a trim under 256 it cannot leave 32 bits. */
        return value + (mul_u32_u16(value, (uint16_t)trim_q8) >> 8);
    }

    delta = mul_u32_u16(value, (uint16_t)(-trim_q8)) >> 8;
    return (delta >= value) ? 0u : value - delta;
}

uint16_t compute_power_d(const decode_state_t *st, uint16_t torque_d)
{
    /* power [kW] = torque [Nm] * rpm / 9550, rearranged for the scaled units.
     * The MFD15 cannot do this itself -- math channels only exist on the
     * MFD28 and MFD32.
     *
     * The torque comes in from the caller because it is transmitted as well,
     * so computing it here too was 1,042 cycles of the gather slot spent
     * getting the same answer a second time. Every gate -- cranking, idle,
     * overrun -- is inside compute_torque_d(), and each of them returns zero,
     * which is exactly what makes this return zero. */
    uint32_t rpm = decode_rpm(st);
    /* rpm comes from a uint16 quarter-count shifted down by two, so it is
     * under 16384 and fits the uint16 mul_u32_u16 takes. */
    return clamp_u16(div_const_round(mul_u32_u16(mul_u32_u16(torque_d, 10u),
                                                 (uint16_t)rpm),
                                     POWER_DIVISOR / 2u, DIVC_95500), 0xFFFFu);
}

/* --- engine health, 0x604 ----------------------------------------------- */

static uint8_t sat_u8(uint32_t v)
{
    return (v > HEALTH_SAT) ? (uint8_t)HEALTH_SAT : (uint8_t)v;
}

/* THE IDLE GRADE. roughness() in tools/idledips.py, line for line, and the
 * order of the lines matters as much as their content -- the host diff holds
 * the two to the same byte over every timestamped fixture. config.h, 0x604,
 * has the reasoning behind every constant; what is here is only the order. */
static void idle_grade(health_t *h, const decode_state_t *st, uint32_t now_ms)
{
    uint16_t rpm_q4 = st->rpm_q4;
    uint32_t baseline;
    bool     settled;

    /* The gate: standing, pedal released, engine turning. The same two
     * thresholds as the torque rule, as a strict complement of it. Leaving it
     * forgets the baseline and the settle clock, but NOT the grade: the grade
     * belongs to the start, and a drive between two idles is part of one. */
    if (st->speed_mmh > STANDSTILL_MMH || st->throttle > THROTTLE_REST ||
        rpm_q4 == 0u) {
        h->in_gate = false;
        h->have_prev_ms = false;
        h->have_prev_rpm = false;
        h->idling = false;
        return;
    }

    if (!h->in_gate) {
        h->in_gate = true;
        h->idle_since_ms = now_ms;
        h->base = (uint32_t)rpm_q4 << IDLE_BASE_SHIFT;
    }
    baseline = h->base >> IDLE_BASE_SHIFT;          /* a shift of 8: free */
    settled = elapsed(now_ms, h->idle_since_ms) >= (uint32_t)IDLE_SETTLE_MS;

    /* Settling means QUIET, not elapsed time: an excursion restarts it.
     * "baseline - rpm >= trip", written without a signed subtraction: all
     * unsigned, so it is byte arithmetic on this part rather than a signed
     * 32-bit compare. */
    if (!settled && baseline >= (uint32_t)rpm_q4 + IDLE_TRIP_RPM * 4u) {
        h->idle_since_ms = now_ms;
    }

    if (settled) {
        if (h->have_prev_ms) {
            h->idle_ms += elapsed(now_ms, h->prev_ms);
        }
        /* One step per CHANGE of the field: a repeated value is the ECU
         * holding its last 180-degree window, not a firing event. */
        if (h->have_prev_rpm && rpm_q4 != h->prev_rpm_q4) {
            uint16_t diff = (rpm_q4 > h->prev_rpm_q4)
                          ? (uint16_t)(rpm_q4 - h->prev_rpm_q4)
                          : (uint16_t)(h->prev_rpm_q4 - rpm_q4);
            uint16_t step = (diff > ROUGH_DEADBAND_RPM * 4u)
                          ? (uint16_t)(diff - ROUGH_DEADBAND_RPM * 4u) : 0u;
            h->rough_acc = h->rough_acc + step - (h->rough_acc >> ROUGH_SHIFT);
        }
    }
    h->prev_ms = now_ms;
    h->have_prev_ms = true;
    if (!h->have_prev_rpm || rpm_q4 != h->prev_rpm_q4) {
        h->prev_rpm_q4 = rpm_q4;
        h->have_prev_rpm = true;
    }
    h->idling = settled;

    /* The baseline steps on ARRIVAL, every frame, because it is a time
     * constant -- the opposite of the grade above, and deliberately so.
     * base + rpm - (base >> 8) never goes below zero, so the unsigned
     * wrap-around of the intermediate is exact. */
    h->base = h->base + rpm_q4 - baseline;
}

/* THE START. start_fields() in tools/idledips.py is the oracle. */
static void start_watch(health_t *h, const decode_state_t *st, uint32_t now_ms)
{
    uint16_t rpm = (uint16_t)(st->rpm_q4 >> 2);

    if (st->rpm_q4 == 0u) {
        if (h->start_phase == HEALTH_START_DIPWIN) {
            h->start_dip = sat_u8(h->fire_rpm);     /* stalled: all the way */
        }
        h->start_phase = HEALTH_START_STOPPED;
        return;
    }

    if (h->start_phase == HEALTH_START_UNKNOWN) {
        h->start_phase = HEALTH_START_RUNNING;      /* already turning */
        return;
    }

    if (h->start_phase == HEALTH_START_STOPPED) {
        /* A new start. Everything about the last one goes, including the
         * grade: an unconverged grade reads healthy, and this is where the
         * convergence clock has to start again from. */
        h->start_phase = HEALTH_START_CRANKING;
        h->start_seen = true;
        h->start_ms = now_ms;
        h->start_crank = HEALTH_UNKNOWN;
        h->start_dip = HEALTH_UNKNOWN;
        h->start_clt = HEALTH_UNKNOWN;
        h->rough_acc = 0u;
        h->idle_ms = 0u;
    }

    if (h->start_phase == HEALTH_START_CRANKING) {
        if (rpm >= START_FIRED_RPM) {
            h->start_crank = sat_u8(elapsed(now_ms, h->start_ms) >>
                                    START_CRANK_SHIFT);
            /* C + 50, from hundredths: raw * 0.75 - 48 + 50 is never
             * negative, and this runs once per start. */
            h->start_clt = (st->clt_c100 == DECODE_TEMP_INVALID)
                ? (uint8_t)HEALTH_UNKNOWN
                : (uint8_t)div_const((uint32_t)((int32_t)st->clt_c100 + 5000),
                                     DIVC_100);
            h->start_phase = HEALTH_START_DIPWIN;
            h->start_ms = now_ms;
            h->fire_rpm = rpm;
            h->low_rpm = rpm;
        }
        return;
    }

    if (h->start_phase == HEALTH_START_DIPWIN) {
        if (elapsed(now_ms, h->start_ms) >= (uint32_t)START_DIP_MS) {
            h->start_dip = sat_u8((uint32_t)(h->fire_rpm - h->low_rpm));
            h->start_phase = HEALTH_START_RUNNING;
        } else if (rpm < h->low_rpm) {
            h->low_rpm = rpm;
        }
    }
}

void compute_on_engine(compute_t *c, const decode_state_t *st, uint32_t now_ms)
{
    /* The start first: a new start clears the grade. The frame that began it
     * cannot be graded against the previous start anyway -- the frame before
     * it was a zero, which closed the gate -- so the order is belt and
     * braces rather than a fix. */
    start_watch(&c->health, st, now_ms);
    idle_grade(&c->health, st, now_ms);
}

uint8_t compute_idle_rough(const compute_t *c)
{
    /* Nothing graded yet this start reads "not known", never zero: zero is a
     * perfectly smooth engine, the one wrong answer that would be believed. */
    if (c->health.idle_ms == 0u) {
        return (uint8_t)HEALTH_UNKNOWN;
    }
    return sat_u8(c->health.rough_acc >> ROUGH_OUT_SHIFT);
}

uint8_t compute_idle_health(const compute_t *c)
{
    uint16_t idx;

    if (c->health.idle_ms < (uint32_t)IDLE_CONVERGE_S * 1000u) {
        return (uint8_t)HEALTH_UNKNOWN;
    }
    /* 100/64 is 25/16: a uint8 x uint8 product and a shift, no division.
     * The rough byte saturates at 254, and 254 x 25 >> 4 is 396, so the
     * product fits a uint16 and the clamp below is what bounds it. */
    idx = (uint16_t)(((uint16_t)compute_idle_rough(c) * 25u) >> 4);
    return (idx > IDLE_INDEX_MAX) ? (uint8_t)IDLE_INDEX_MAX : (uint8_t)idx;
}

uint8_t compute_idle_s(const compute_t *c)
{
    uint32_t s = div_const(c->health.idle_ms, DIVC_1000);

    return (s > 255u) ? 255u : (uint8_t)s;
}
