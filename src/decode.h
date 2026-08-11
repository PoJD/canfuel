/* decode.h -- parsing the powertrain bus into a state struct.
 *
 * PURE C. No <xc.h>, no hardware, no globals. It takes an identifier, a
 * payload and a length, and folds them into a struct. That is what makes the
 * whole brain of the device testable against real logs on a PC.
 *
 * The signal table this implements is docs/can-decoding.md.
 */
#ifndef DECODE_H
#define DECODE_H

#include <stdbool.h>
#include <stdint.h>

/* Returned by the temperature fields when the sensor reports 0xFF. It is
 * outside any physical range, so it can never collide with a reading. */
#define DECODE_TEMP_INVALID     ((int16_t)-32768)

typedef struct {
    /* Engine, from 0x280. rpm is kept in quarter-rpm because that is the raw
     * resolution and because the restart test needs an exact zero. */
    uint16_t rpm_q4;            /* 0.25 rpm                                 */
    uint16_t torque_ind_cnm;    /* 0.01 Nm, indicated, drag not yet removed */
    uint8_t  throttle;          /* raw, 38 = rest position                  */
    uint8_t  load;              /* raw, 0 with the engine off               */

    /* Road speed, from 0x1A0. The value is only updated while the gate in
     * byte 1 passes, so a stale reading survives the init ramp instead of
     * being replaced by garbage -- but speed_valid drops. */
    uint32_t speed_mmh;         /* 0.001 km/h                               */
    bool     speed_valid;

    /* Temperatures, DECODE_TEMP_INVALID when the sensor reports 0xFF. */
    int16_t  clt_c100;          /* 0.01 C, from 0x288 b1                    */
    int16_t  oil_c100;          /* 0.01 C, from 0x420 b3                    */

    /* Tank, from 0x320 b2. Seven bits of litres plus the reserve lamp. */
    uint8_t  tank_l;
    bool     tank_reserve;

    /* Lateral acceleration, from 0x5A0 b0. Positive is a left-hand turn,
     * measured in the car on 2026-08-11 -- docs/can-decoding.md question 5. */
    int16_t  accel_mg;          /* 0.001 g                                  */

    /* The fuel counter, from 0x480 b2-b3. Already masked to 15 bits;
     * counter_wrapped carries bit 15, which is a "this ignition cycle has
     * wrapped at least once" flag and not part of the number. */
    uint16_t fuel_counter;
    bool     fuel_counter_valid; /* false until the first 0x480 arrives     */
    bool     counter_wrapped;
} decode_state_t;

/* Zero state: no readings yet, speed invalid, temperatures invalid. */
void decode_init(decode_state_t *st);

/* Fold one frame in. Returns true when the identifier was one we care about
 * and the payload was long enough to use.
 *
 * dlc is honoured rather than assumed: 0x050 carries 4 bytes and 0x5D0 six,
 * so a parser hardcoding 8 would read past the end of those.
 */
bool decode_frame(decode_state_t *st, uint16_t can_id,
                  const uint8_t *data, uint8_t dlc);

/* Whole rpm, for the places that want a human number rather than quarters.
 *
 * This was a `static inline' in the header until the first XC8 build, which
 * emits an out-of-line copy of it into every translation unit that includes
 * decode.h and then warns (2053) about the copies nobody calls -- three
 * warnings on every build, which is exactly enough noise to hide a real one.
 * As an ordinary function it is one call for one shift, on a path that runs
 * twice per 0x480 frame, i.e. twice per 10 ms. */
uint16_t decode_rpm(const decode_state_t *st);

#endif /* DECODE_H */
