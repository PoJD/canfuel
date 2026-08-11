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

    v->power_d  = compute_power_d(st);
    v->torque_d = compute_torque_d(st);
    v->flow_c   = compute_flow_lh_c(c);

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

void txframes_trip(const tx_values_t *v, uint8_t *out)
{
    put_be32(out + 0, v->trip_ml);
    put_be32(out + 4, v->trip_m);
}
