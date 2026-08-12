/* txframes.h -- assembling the three frames we put on the bus. PURE C.
 *
 * Everything is unsigned big endian. The car is little endian throughout and
 * we are deliberately not, so a byte order mistake shows up as an absurd
 * number rather than as a plausible one.
 *
 * The layout is docs/frames.md and it is consumed by mfd15/tri/S-AQY.TRI,
 * which is already uploaded to a real display. Changing the layout here means
 * changing it there in the same breath -- a mismatch produces no error at
 * all, just wrong numbers that look right.
 */
#ifndef TXFRAMES_H
#define TXFRAMES_H

#include <stdbool.h>
#include <stdint.h>

#include "compute.h"
#include "decode.h"

#define TXFRAME_DLC     8

/* Everything the three frames carry, already in the unit of the wire. Pulled
 * out into a struct so the assembly can be tested without an accumulator and
 * so main.c gathers once and transmits three times. */
typedef struct {
    /* 0x600 */
    uint16_t fuel_now_d;        /* 0.1, l/h or l/100 km depending on speed */
    uint16_t fuel_avg_d;        /* 0.1 l/100 km                            */
    uint16_t fuel_tank_d;       /* 0.1 l, damped                           */
    uint16_t range_km;          /* 1 km                                    */
    /* 0x601 */
    uint16_t power_d;           /* 0.1 kW                                  */
    uint16_t torque_d;          /* 0.1 Nm, drag already removed            */
    uint16_t flow_c;            /* 0.01 l/h                                */
    uint16_t vdd_c;             /* 0.01 V, measured by the PIC on itself   */
    /* 0x602 */
    uint32_t trip_ml;           /* 0.001 l since the last reset            */
    uint32_t trip_m;            /* metres since the last reset             */
} tx_values_t;

/* Read everything out of the core into transmit units.
 *
 * vdd_c comes from hal_sys and is passed in rather than read, so this stays
 * pure. When the bus has been quiet for longer than DATA_TIMEOUT_MS every
 * value derived from it goes to zero -- see txframes.c for why vdd_c does not.
 */
void txframes_gather(tx_values_t *v, const compute_t *c,
                     const decode_state_t *st, uint16_t vdd_c, uint32_t now_ms);

/* The two trip totals of 0x602, which is transmitted once a second while the
 * gather above runs ten times a second. Call it immediately before
 * txframes_trip(): the gather clears the whole struct, so these do not
 * survive the next fast slot. Obeys the same quiet-bus rule as the gather. */
void txframes_gather_trip(tx_values_t *v, const compute_t *c, uint32_t now_ms);

/* Each writes exactly TXFRAME_DLC bytes. */
void txframes_fuel(const tx_values_t *v, uint8_t *out);     /* 0x600, 100 ms */
void txframes_engine(const tx_values_t *v, uint8_t *out);   /* 0x601, 100 ms */
void txframes_trip(const tx_values_t *v, uint8_t *out);     /* 0x602, 1 s    */

#endif /* TXFRAMES_H */
