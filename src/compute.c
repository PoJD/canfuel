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
    c->flow_head = 0;
    c->flow_count = 0;
    c->flow_sum_ul = 0;
    c->flow_sum_ms = 0;
    c->flow_ul_s = 0;
}

static void flow_drop_oldest(compute_t *c)
{
    flow_sample_t *s = &c->flow[c->flow_head];
    c->flow_sum_ul -= s->ul;
    c->flow_sum_ms -= s->ms;
    c->flow_head = (uint8_t)((c->flow_head + 1u) % FLOW_WINDOW_SLOTS);
    c->flow_count--;
}

/* ! HOT PATH. Runs on every 0x480, which is ~26 times a second. Read
 * ! docs/optimisation.md before adding anything to it -- especially a
 * ! division, which costs 1,026 cycles on this part. */
static void flow_push(compute_t *c, uint16_t ul, uint16_t ms)
{
    uint8_t tail;

    if (c->flow_count == FLOW_WINDOW_SLOTS) {
        /* Only reachable when 0x480 bunches up far tighter than the ~38 ms
         * it averages at idle -- duplicate frames in a log do exactly that,
         * and the frame has no fixed period to begin with. Dropping the
         * oldest is what the window would have done a moment later anyway. */
        flow_drop_oldest(c);
    }

    tail = (uint8_t)((c->flow_head + c->flow_count) % FLOW_WINDOW_SLOTS);
    c->flow[tail].ul = ul;
    c->flow[tail].ms = ms;
    c->flow_count++;
    c->flow_sum_ul += ul;
    c->flow_sum_ms += ms;

    /* Keep roughly one second in the window. Without it the number on the
     * display dances at the frame rate; with a longer one it lags the pedal. */
    while (c->flow_sum_ms > FLOW_WINDOW_MS && c->flow_count > 1u) {
        flow_drop_oldest(c);
    }

    c->flow_ul_s = div_round(mul_u32_u16(c->flow_sum_ul, 1000u), c->flow_sum_ms);
}

/* --- the tank median ---------------------------------------------------- */

/* The median of the ring, read out of a bucket histogram instead of by
 * sorting it.
 *
 * ! HOT LOOP. READ docs/optimisation.md BEFORE CHANGING THIS. Cycles are
 * ! expensive on a 4 MIPS part with no cache and no hardware divide, and this
 * ! function was the most expensive thing in the core until 2026-08-11. The
 * ! types and the walking pointer below are load-bearing, not style.
 *
 * WHY NOT A SORT. This used to be an insertion sort over the 25 slots, and it
 * was the single most expensive thing in the core: 300 comparisons and moves
 * in the worst case, plus a 25-byte memcpy, 15,068 cycles or 3.77 ms. It was
 * also the only cost in the whole firmware that depended on the *data* rather
 * than on the code -- a reversed ring cost twelve times a sorted one -- and
 * a bound you can only reach on unlucky input is a bound that gets forgotten.
 *
 * WHY A HISTOGRAM WORKS HERE. We never want the sorted array, only the middle
 * element, and the value being sorted is 0x320 b2 masked to seven bits: a
 * tank level of 0..127. That is a small, fixed, known key space, so counting
 * beats comparing. tank_sample() keeps the buckets up to date as samples go
 * in and out of the ring, which leaves this function a single sweep with no
 * branches worth the name and no worst case worth quoting.
 *
 * WHY IT IS THE SAME ANSWER. The sort returned sorted[n/2] -- for an even n
 * that is the upper of the two middle elements, which is what the running sum
 * below also lands on. The first bucket whose cumulative count exceeds n/2 is
 * by definition the bucket that index n/2 falls in. test_compute.c pins this
 * against the fixtures. */
static uint8_t tank_median(const compute_t *c)
{
    /* Both of these types are load-bearing on an 8-bit part, and both are
     * safe: the ring holds at most TANK_MEDIAN_SLOTS = 25 samples, so neither
     * the running total nor the target can leave a byte. Written as uint16_t
     * the comparison alone costs six extra instructions per bucket.
     *
     * The walking pointer is the other half of it. Indexing tank_bins[v]
     * makes XC8 rebuild the address from the struct base on every iteration --
     * twelve instructions of lfsr and add -- where a pointer it can simply
     * increment costs one. */
    const uint8_t *bin = c->tank_bins;
    uint8_t target = (uint8_t)(c->tank_hist_count / 2u);
    uint8_t cum = 0;
    uint8_t v;

    for (v = 0; v < (uint8_t)TANK_HIST_BINS; v++) {
        cum = (uint8_t)(cum + *bin++);
        if (cum > target) {
            return v;
        }
    }
    return 0;   /* only reachable with an empty ring, which the caller gates */
}

static void tank_sample(compute_t *c, const decode_state_t *st)
{
    uint32_t target_ml = mul_u32_u16(st->tank_l, 1000u);

    /* The displayed level is damped whether we are moving or not -- that is
     * what the damping is for. First order, one sample a second, so the time
     * constant is TANK_DAMP_SAMPLES seconds. */
    if (!c->tank_damped_valid) {
        c->tank_damped_ml = target_ml;
        c->tank_damped_valid = true;
    } else if (target_ml > c->tank_damped_ml) {
        c->tank_damped_ml += div_const(target_ml - c->tank_damped_ml, DIVC_120);
    } else {
        c->tank_damped_ml -= div_const(c->tank_damped_ml - target_ml, DIVC_120);
    }

    /* The median that the refuelling rule watches is only fed while standing.
     * While driving the float sloshes over a 9-10 L spread on every corner,
     * so the reading is worthless; at rest one litre dominates completely.
     * docs/refuel-reset.md has the measurement. */
    if (st->speed_mmh >= TANK_STATIONARY_MMH) {
        return;
    }

    /* Keep the histogram in step with the ring. Once the ring is full the slot
     * about to be overwritten still holds a sample that is counted, so it has
     * to come out of its bucket first; until then the slot is untouched and
     * there is nothing to remove. tank_l is masked to seven bits by decode.c,
     * so it can never index outside tank_bins. */
    if (c->tank_hist_count == TANK_MEDIAN_SLOTS) {
        c->tank_bins[c->tank_hist[c->tank_hist_next]]--;
    }
    c->tank_hist[c->tank_hist_next] = st->tank_l;
    c->tank_bins[st->tank_l]++;

    /* A compare rather than a modulo: TANK_MEDIAN_SLOTS is 25, so % is a real
     * division on this part rather than a mask. */
    if (++c->tank_hist_next >= (uint8_t)TANK_MEDIAN_SLOTS) {
        c->tank_hist_next = 0;
    }
    if (c->tank_hist_count < TANK_MEDIAN_SLOTS) {
        c->tank_hist_count++;
    }
    if (c->tank_hist_count < TANK_MEDIAN_MIN) {
        return;
    }

    {
        uint8_t median = tank_median(c);

        if (!c->tank_stable_valid) {
            /* First ever stable reading, or the first after an empty EEPROM.
             * Initialise only -- resetting here would clear the average every
             * time the device is powered up. */
            c->tank_stable_valid = true;
        } else if (median > c->tank_stable_l &&
                   (uint8_t)(median - c->tank_stable_l) > REFUEL_RISE_L) {
            compute_reset_trip(c);
            c->refuels++;
            /* Snap the damped level to the median rather than letting the
             * filter crawl up to it. A refuelling is the one change in tank
             * level that is both large and instantaneous, and it is the one
             * moment the driver is certain to look at the gauge. The median at
             * rest is the most trustworthy number we have about the tank, so
             * there is nothing to gain by approaching it slowly. Without this
             * the level and the range would both read minutes-old for minutes
             * after filling up. */
            c->tank_damped_ml = mul_u32_u16(median, 1000u);
        }
        c->tank_stable_l = median;
    }
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
    memset(c->seg_ul, 0, sizeof c->seg_ul);
    c->seg_next = 0;
    c->seg_count = 0;
    c->seg_cur_ul = 0;
    c->seg_cur_mm = 0;
}

void compute_restore(compute_t *c, uint32_t total_ul, uint32_t total_mm,
                     uint8_t tank_stable_l, bool tank_stable_valid)
{
    c->total_ul = total_ul;
    c->total_mm = total_mm;
    c->tank_stable_l = tank_stable_l;
    c->tank_stable_valid = tank_stable_valid;
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

    if (dt_ms > 0u && dt_ms <= 0xFFFFu) {
        flow_push(c, delta_ul, (uint16_t)dt_ms);
    } else if (dt_ms > 0xFFFFu) {
        /* Over a minute without a frame. Whatever the window held describes a
         * different situation entirely. */
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
                c->seg_ul[c->seg_next] = c->seg_cur_ul;
                /* Compare, not modulo -- RANGE_SEGMENTS is 30. */
                if (++c->seg_next >= (uint8_t)RANGE_SEGMENTS) {
                    c->seg_next = 0;
                }
                if (c->seg_count < RANGE_SEGMENTS) {
                    c->seg_count++;
                }
                c->seg_cur_ul = 0;
                c->seg_cur_mm -= RANGE_SEGMENT_MM;
            }
        }
    }

    if (elapsed(now_ms, c->last_tank_ms) >= TANK_SAMPLE_MS) {
        c->last_tank_ms = now_ms;
        tank_sample(c, st);
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

    /* The rolling window is over whole kilometres, so below RANGE_MIN_MM it
     * has too few slots to mean anything and a conservative fixed figure is
     * used instead. */
    if (c->total_mm >= RANGE_MIN_MM && c->seg_count > 0u) {
        uint32_t sum = 0;
        uint8_t i;
        for (i = 0; i < c->seg_count; i++) {
            sum += c->seg_ul[i];
        }
        /* Again microlitres per metre: seg_count kilometres is seg_count*1000
         * metres. */
        basis_d = div_round(sum, mul_u32_u16(c->seg_count, 1000u));
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

    drag_cnm = (uint32_t)DRAG_TORQUE_BASE_CNM +
               div_const(mul_u32_u16(rpm, (uint16_t)DRAG_TORQUE_SLOPE_E4),
                         DIVC_10000);

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
