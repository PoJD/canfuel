/* compute.c -- see compute.h. PURE C, no hardware.
 *
 * The traps this file exists to avoid are written up in docs/can-decoding.md.
 * Three of the four live in here: the restart rule, the modulo delta and the
 * minimum distance under the average.
 */

#include <string.h>

#include "compute.h"

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

static void flow_push(compute_t *c, uint16_t ul, uint16_t ms)
{
    uint8_t tail;

    if (c->flow_count == FLOW_WINDOW_SLOTS) {
        /* Only reachable when 0x480 arrives far faster than its 49.5 ms --
         * duplicate frames in a log do exactly that. Dropping the oldest is
         * what the window would have done a moment later anyway. */
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

    c->flow_ul_s = div_round(c->flow_sum_ul * 1000u, c->flow_sum_ms);
}

/* --- the tank median ---------------------------------------------------- */

static uint8_t tank_median(const compute_t *c)
{
    uint8_t sorted[TANK_MEDIAN_SLOTS];
    uint8_t n = c->tank_hist_count;
    uint8_t i, j;

    memcpy(sorted, c->tank_hist, n);
    for (i = 1; i < n; i++) {          /* insertion sort, n is at most 25 */
        uint8_t key = sorted[i];
        j = i;
        while (j > 0u && sorted[j - 1u] > key) {
            sorted[j] = sorted[j - 1u];
            j--;
        }
        sorted[j] = key;
    }
    return sorted[n / 2u];
}

static void tank_sample(compute_t *c, const decode_state_t *st)
{
    uint32_t target_ml = (uint32_t)st->tank_l * 1000u;

    /* The displayed level is damped whether we are moving or not -- that is
     * what the damping is for. First order, one sample a second, so the time
     * constant is TANK_DAMP_SAMPLES seconds. */
    if (!c->tank_damped_valid) {
        c->tank_damped_ml = target_ml;
        c->tank_damped_valid = true;
    } else if (target_ml > c->tank_damped_ml) {
        c->tank_damped_ml += (target_ml - c->tank_damped_ml) / TANK_DAMP_SAMPLES;
    } else {
        c->tank_damped_ml -= (c->tank_damped_ml - target_ml) / TANK_DAMP_SAMPLES;
    }

    /* The median that the refuelling rule watches is only fed while standing.
     * While driving the float sloshes over a 9-10 L spread on every corner,
     * so the reading is worthless; at rest one litre dominates completely.
     * docs/refuel-reset.md has the measurement. */
    if (st->speed_mmh >= TANK_STATIONARY_MMH) {
        return;
    }

    c->tank_hist[c->tank_hist_next] = st->tank_l;
    c->tank_hist_next = (uint8_t)((c->tank_hist_next + 1u) % TANK_MEDIAN_SLOTS);
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
        c->have_tank_ms = true;
        return;
    }

    dt_ms = elapsed(now_ms, c->last_tick_ms);
    c->last_tick_ms = now_ms;

    /* v [0.001 km/h] * t [ms] / 3600 = s [mm]. A gap longer than a second
     * means we were not watching, and guessing across it would invent
     * distance the car may never have covered. */
    if (st->speed_valid && st->speed_mmh > 0u && dt_ms > 0u && dt_ms <= 1000u) {
        uint32_t mm = st->speed_mmh * dt_ms / 3600u;
        c->total_mm += mm;
        c->seg_cur_mm += mm;

        while (c->seg_cur_mm >= RANGE_SEGMENT_MM) {
            c->seg_ul[c->seg_next] = c->seg_cur_ul;
            c->seg_next = (uint8_t)((c->seg_next + 1u) % RANGE_SEGMENTS);
            if (c->seg_count < RANGE_SEGMENTS) {
                c->seg_count++;
            }
            c->seg_cur_ul = 0;
            c->seg_cur_mm -= RANGE_SEGMENT_MM;
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
    return clamp_u16(div_round(c->flow_ul_s * 36u, 100u), 0xFFFFu);
}

uint16_t compute_fuel_now_d(const compute_t *c, const decode_state_t *st)
{
    /* Dual unit, a single threshold and no hysteresis: the jump when it
     * switches is the visual cue that it switched. Without a trustworthy
     * speed, l/100 km is meaningless, so l/h is sent. */
    if (!st->speed_valid || st->speed_mmh < FUELNOW_LH_BELOW_MMH) {
        /* l/h at 0.1 = ul/s * 3.6 / 100 */
        return clamp_u16(div_round(c->flow_ul_s * 36u, 1000u), FUELNOW_CLAMP_D);
    }
    /* l/100 km at 0.1 = ul/s * 3600 / v[0.001 km/h] */
    return clamp_u16(div_round(c->flow_ul_s * 3600u, st->speed_mmh),
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
    return clamp_u16(div_round(c->total_ul, c->total_mm / 1000u),
                     FUELNOW_CLAMP_D);
}

uint16_t compute_tank_d(const compute_t *c)
{
    return clamp_u16(div_round(c->tank_damped_ml, 100u), 0xFFFFu);
}

uint16_t compute_range_km(const compute_t *c, const decode_state_t *st)
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
        basis_d = div_round(sum, (uint32_t)c->seg_count * 1000u);
        if (basis_d == 0u) {
            basis_d = RANGE_DEFAULT_L100_D;
        }
    }

    /* km = litres / (l/100 km) * 100, and basis is in tenths. */
    return clamp_u16((uint32_t)st->tank_l * 1000u / basis_d, 0xFFFFu);
}

uint32_t compute_trip_ml(const compute_t *c)
{
    return c->total_ul / 1000u;
}

uint32_t compute_trip_m(const compute_t *c)
{
    return c->total_mm / 1000u;
}

uint16_t compute_torque_d(const decode_state_t *st)
{
    /* Drag torque -- friction, pumps, alternator -- is not constant; it rises
     * with engine speed and is modelled linearly. Both calibration points come
     * out of the fixtures, see config.h. */
    uint32_t rpm = decode_rpm(st);
    uint32_t drag_cnm = (uint32_t)DRAG_TORQUE_BASE_CNM +
                        rpm * (uint32_t)DRAG_TORQUE_SLOPE_E4 / 10000u;
    uint32_t net_cnm;

    if (st->torque_ind_cnm <= drag_cnm) {
        return 0;               /* on the overrun the engine is being driven */
    }
    net_cnm = st->torque_ind_cnm - drag_cnm;
    return clamp_u16(div_round(net_cnm, 10u), 0xFFFFu);
}

uint16_t compute_power_d(const decode_state_t *st)
{
    /* power [kW] = torque [Nm] * rpm / 9550, rearranged for the scaled units.
     * The MFD15 cannot do this itself -- math channels only exist on the
     * MFD28 and MFD32. */
    uint32_t rpm = decode_rpm(st);
    uint32_t torque_d = compute_torque_d(st);
    return clamp_u16(div_round(torque_d * 10u * rpm, POWER_DIVISOR), 0xFFFFu);
}
