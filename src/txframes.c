/* txframes.c -- see txframes.h. PURE C, no hardware. */

#include <string.h>

#include "txframes.h"

/* Big endian, high byte first. One place, so there is one thing to get wrong
 * and one place to check it. */
static void put_be16(uint8_t *p, uint16_t v)
{
    p[0] = (uint8_t)(v >> 8);
    p[1] = (uint8_t)(v & 0xFFu);
}

static void put_be32(uint8_t *p, uint32_t v)
{
    p[0] = (uint8_t)(v >> 24);
    p[1] = (uint8_t)(v >> 16);
    p[2] = (uint8_t)(v >> 8);
    p[3] = (uint8_t)(v & 0xFFu);
}

/* ! THE MOST EXPENSIVE FUNCTION IN THE FIRMWARE: 6.4 ms, almost all of it nine
 * ! 32-bit divisions at 1,026 cycles each. Read docs/optimisation.md before
 * ! adding a getter here, and prefer arranging the arithmetic so a division
 * ! disappears over making the division faster. */
void txframes_gather(tx_values_t *v, const compute_t *c,
                     const decode_state_t *st, uint16_t vdd_c, uint32_t now_ms)
{
    memset(v, 0, sizeof *v);

    /* The supply voltage is the one thing here that does not come off the
     * bus -- the PIC measures it on itself through the internal 1.024 V
     * reference. It stays live when the bus goes quiet, deliberately: a dead
     * bus is exactly the moment you want to know whether the converter is
     * still being fed. docs/frames.md says so too. */
    v->vdd_c = vdd_c;

    if (!compute_data_live(c, now_ms)) {
        /* Freezing the last reading would put a plausible, wrong number in
         * front of the driver. Zero is unmistakable. */
        return;
    }

    v->fuel_now_d  = compute_fuel_now_d(c, st);
    v->fuel_avg_d  = compute_avg_l100_d(c);
    v->fuel_tank_d = compute_tank_d(c);
    v->range_km    = compute_range_km(c);

    /* Torque first and then power from it: they are the same number and both
     * go on the wire, so power no longer computes it again. */
    v->torque_d = compute_torque_d(st);
    v->power_d  = compute_power_d(st, v->torque_d);
    v->flow_c   = compute_flow_lh_c(c);
}

/* The trip totals live here rather than in the gather because 0x602 is
 * transmitted once a second while the gather runs ten times a second: two
 * divisions by 1000, 686 cycles, were being computed nine times out of ten for
 * nobody to read.
 *
 * main.c calls this immediately before txframes_trip(), which is the only
 * arrangement that works -- txframes_gather() clears the whole struct, so a
 * value put here does not survive the next fast slot and is not meant to. */
void txframes_gather_trip(tx_values_t *v, const compute_t *c, uint32_t now_ms)
{
    if (!compute_data_live(c, now_ms)) {
        /* The same rule as the gather, for the same reason: a quiet bus
         * transmits zero rather than a stale number that looks plausible. */
        v->trip_ml = 0;
        v->trip_m = 0;
        return;
    }

    v->trip_ml = compute_trip_ml(c);
    v->trip_m  = compute_trip_m(c);
}

void txframes_fuel(const tx_values_t *v, uint8_t *out)
{
    put_be16(out + 0, v->fuel_now_d);
    put_be16(out + 2, v->fuel_avg_d);
    put_be16(out + 4, v->fuel_tank_d);
    put_be16(out + 6, v->range_km);
}

void txframes_engine(const tx_values_t *v, uint8_t *out)
{
    put_be16(out + 0, v->power_d);
    put_be16(out + 2, v->torque_d);
    put_be16(out + 4, v->flow_c);
    put_be16(out + 6, v->vdd_c);
}

void txframes_gather_diag(tx_values_t *v, uint8_t rx_err, uint8_t tx_err,
                          uint8_t can_status, uint8_t flags,
                          uint8_t reset_cause, uint8_t tx_fail,
                          uint16_t uptime_s)
{
    /* No compute_data_live() gate here, deliberately -- see txframes.h. */
    v->diag_rx_err      = rx_err;
    v->diag_tx_err      = tx_err;
    v->diag_can_status  = can_status;
    v->diag_flags       = flags;
    v->diag_reset_cause = reset_cause;
    v->diag_tx_fail     = tx_fail;
    v->diag_uptime_s    = uptime_s;
}

void txframes_trip(const tx_values_t *v, uint8_t *out)
{
    put_be32(out + 0, v->trip_ml);
    put_be32(out + 4, v->trip_m);
}

void txframes_diag(const tx_values_t *v, uint8_t *out)
{
    out[0] = v->diag_rx_err;
    out[1] = v->diag_tx_err;
    out[2] = v->diag_can_status;
    out[3] = v->diag_flags;
    out[4] = (uint8_t)((v->diag_reset_cause & DIAG_RESET_CAUSE_MASK) |
                       (DIAG_LAYOUT_VERSION << DIAG_VERSION_SHIFT));
    out[5] = v->diag_tx_fail;
    put_be16(out + 6, v->diag_uptime_s);
}
