/* compute.c -- see compute.h. PURE C, no hardware.
 *
 * The traps this file exists to avoid are written up in docs/can-decoding.md.
 * Three of the four live in here: the restart rule, the modulo delta and the
 * minimum distance under the average.
 */

#include <string.h>

#include "compute.h"
#include "divconst.h"

/* --- helpers ------------------------------------------------------------ */

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
 * ! docs/optimisation.md before adding anything to it -- especially a
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
 * one of the divisors with a free shift in divconst.h. */
static void range_basis_update(compute_t *c)
{
    uint16_t km_q4 = (uint16_t)(clamp_u16(div_const(c->seg_cur_ul, DIVC_1000),
                                          FUELNOW_CLAMP_D) << RANGE_BASIS_Q4);

    if (c->basis_q4 == 0u) {
        /* The first kilometre of a trip has nothing to average against, so it
         * is the whole estimate. A kilometre that burned nothing at all --
         * possible on a long descent, where the ECU cuts the injectors --
         * leaves the basis at zero and Range keeps the conservative default,
         * which is the right way to be wrong about it. */
        c->basis_q4 = km_q4;
        return;
    }
    if (km_q4 > c->basis_q4) {
        c->basis_q4 = (uint16_t)(c->basis_q4 +
                      ((km_q4 - c->basis_q4) >> RANGE_BASIS_SHIFT));
    } else {
        c->basis_q4 = (uint16_t)(c->basis_q4 -
                      ((c->basis_q4 - km_q4) >> RANGE_BASIS_SHIFT));
    }
}

/* --- the tank, and the refuelling trigger -------------------------------- */

static void tank_sample(compute_t *c, const decode_state_t *st)
{
    uint32_t target_ml = mul_u32_u16(st->tank_l, 1000u);
    uint16_t target_q8;

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
     * docs/refuel-reset.md has the measurement. */
    if (st->speed_mmh >= TANK_STATIONARY_MMH) {
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

    /* The settled level: first order over the at-rest samples, in 1/256 l so
     * the step is a shift and not a division. TANK_REST_SHIFT is the time
     * constant in samples, i.e. in seconds. */
    if (target_q8 > c->tank_rest_q8) {
        c->tank_rest_q8 = (uint16_t)(c->tank_rest_q8 +
                          ((target_q8 - c->tank_rest_q8) >> TANK_REST_SHIFT));
    } else {
        c->tank_rest_q8 = (uint16_t)(c->tank_rest_q8 -
                          ((c->tank_rest_q8 - target_q8) >> TANK_REST_SHIFT));
    }
    c->tank_stable_l = (uint8_t)(c->tank_rest_q8 >> 8);
}

/* --- lifecycle ---------------------------------------------------------- */

void compute_init(compute_t *c)
{
    memset(c, 0, sizeof *c);
}

void compute_reset_trip(compute_t *c)
{
    c->total_ul = 0;
    c->total_mm = 0;
    c->seg_cur_ul = 0;
    c->seg_cur_mm = 0;
    /* The basis goes with the trip. It is a property of the driving that was
     * just discarded, and Range falls back to the conservative default until
     * RANGE_MIN_MM of the new trip has been driven -- which is what the old
     * segment ring did when it was cleared here. */
    c->basis_q4 = 0;
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
    uint32_t basis_d = RANGE_DEFAULT_L100_D;

    /* The basis is built a kilometre at a time, so below RANGE_MIN_MM it rests
     * on too few of them to mean anything and a conservative fixed figure is
     * used instead. Zero means no kilometre has completed at all. */
    if (c->total_mm >= RANGE_MIN_MM && c->basis_q4 > 0u) {
        basis_d = (uint32_t)(c->basis_q4 >> RANGE_BASIS_Q4);
        if (basis_d == 0u) {
            basis_d = RANGE_DEFAULT_L100_D;
        }
    }

    /* THE DAMPED LEVEL, NOT THE INSTANTANEOUS ONE. This used to read
     * st->tank_l, which is the raw float position and slosh and all: on
     * 07_accel the raw value swings over 10 L during a pull-away, which is
     * 111 km of range appearing and disappearing several times a second while
     * the level shown right next to it sat still. The damping that
     * compute_tank_d already had is worth exactly as much here, and the two
     * gauges have no business disagreeing about how much fuel is in the tank.
     *
     * The stable median would be steadier still, but it only updates at rest,
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

    /* A STANDING CAR WITH THE THROTTLE SHUT MAKES NO NET TORQUE. THIS RULE IS
     * FIXED AND IS NOT TO BE RELAXED, WHATEVER A FUTURE DRAG REFIT SAYS.
     * The drag line cannot deliver this on its own -- idle sits above it by
     * construction (config.h) -- so it is asserted here instead of fitted.
     * IDLE_GATE_* in config.h holds the two thresholds and the evidence. */
    if (st->speed_mmh <= IDLE_GATE_SPEED_MMH && st->throttle <= THROTTLE_REST) {
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
    return clamp_u16(div_const_round(net_cnm, 5u, DIVC_10), 0xFFFFu);
}

uint16_t compute_power_d(const decode_state_t *st, uint16_t torque_d)
{
    /* power [kW] = torque [Nm] * rpm / 9550, rearranged for the scaled units.
     * The MFD15 cannot do this itself -- math channels only exist on the
     * MFD28 and MFD32.
     *
     * The torque comes in from the caller because it is transmitted as well,
     * so computing it here too was 1,042 cycles of the 100 ms slot spent
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
