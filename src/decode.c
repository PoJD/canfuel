/* decode.c -- see decode.h. PURE C, no hardware.
 *
 * Every formula here is from the table in docs/can-decoding.md and every one
 * of them was measured on the car, not taken from a database.
 */

#include "decode.h"
#include "fastmul.h"
#include "config.h"

/* Little endian on the wire. The car is little endian throughout; only the
 * frames we transmit ourselves are big endian, deliberately, so the two can
 * never be confused. */
static uint16_t u16le(const uint8_t *d, uint8_t i)
{
    return (uint16_t)(d[i] | ((uint16_t)d[i + 1] << 8));
}

/* Both temperature sensors share the same scaling and the same fault value. */
static int16_t temp_c100(uint8_t raw)
{
    if (raw == 0xFFu) {
        return DECODE_TEMP_INVALID;
    }
    return (int16_t)((int16_t)raw * 75 - 4800);   /* raw * 0.75 - 48 C */
}

void decode_init(decode_state_t *st)
{
    st->rpm_q4 = 0;
    st->torque_ind_cnm = 0;
    st->throttle = 0;

    st->speed_mmh = 0;
    st->speed_valid = false;

    st->clt_c100 = DECODE_TEMP_INVALID;
    st->oil_c100 = DECODE_TEMP_INVALID;

    st->tank_l = 0;
    st->tank_valid = false;

    st->fuel_counter = 0;
    st->fuel_counter_valid = false;
}

uint16_t decode_rpm(const decode_state_t *st)
{
    return (uint16_t)(st->rpm_q4 >> 2);
}

bool decode_frame(decode_state_t *st, uint16_t can_id,
                  const uint8_t *data, uint8_t dlc)
{
    switch (can_id) {

    case CAN_ID_ENGINE:
        if (dlc < 8) {
            return false;
        }
        st->rpm_q4 = u16le(data, 2);
        st->throttle = data[5];
        /* Both operands cast to uint16 explicitly: written as a plain
         * data[7] * CONST, XC8 promotes to 32 bits and calls ___lmul for what
         * is an 8x8 product the hardware multiplier does in one cycle. */
        st->torque_ind_cnm = (uint16_t)((uint16_t)data[7] *
                                        (uint16_t)TORQUE_CNM_PER_BIT);
        return true;

    case CAN_ID_SPEED:
        if (dlc < 4) {
            return false;
        }
        /* Byte 1 is a bit field, not a value. 0x40 says the speed is usable;
         * the low two bits mark the ~0.4 s init ramp after ignition on, where
         * the raw value falls 464 -> 0 and means nothing. Bits 0x08 and 0x10
         * carry something else and do not affect validity -- in 07_accel the
         * majority state is in fact 0x48, so testing b1 == 0x40 would discard
         * two thirds of the log. docs/can-decoding.md, trap 1. */
        st->speed_valid = (data[1] & SPEED_GATE_REQUIRED) != 0u &&
                          (data[1] & SPEED_GATE_FORBIDDEN) == 0u;
        if (st->speed_valid) {
            /* raw * 0.005 km/h. mul_u32_u16 rather than a plain multiply for
             * the same reason as everywhere else: XC8 would call ___lmul. */
            st->speed_mmh = mul_u32_u16(u16le(data, 2), 5u);
        }
        return true;

    case CAN_ID_COOLANT:
        if (dlc < 2) {
            return false;
        }
        st->clt_c100 = temp_c100(data[1]);
        return true;

    case CAN_ID_OIL:
        if (dlc < 4) {
            return false;
        }
        st->oil_c100 = temp_c100(data[3]);
        return true;

    case CAN_ID_TANK:
        if (dlc < 3) {
            return false;
        }
        /* Bit 7 is the reserve lamp. It is not decoded: nothing in the
         * firmware or on the display uses it, and the display reads 0x320
         * itself with a 0x7F mask anyway. */
        st->tank_l = (uint8_t)(data[2] & 0x7Fu);
        st->tank_valid = true;
        return true;

    case CAN_ID_FUEL: {
        uint16_t raw;
        if (dlc < 4) {
            return false;
        }
        raw = u16le(data, 2);
        /* Bit 15 is not part of the number and it is not constant either --
         * it is zero from ignition on until the first wrap, then permanently
         * one. The mask drops it and nothing needs it as a flag; trap 3 in
         * docs/can-decoding.md is where that behaviour is recorded. */
        st->fuel_counter = (uint16_t)(raw & COUNTER_MASK);
        st->fuel_counter_valid = true;
        return true;
    }

    default:
        return false;
    }
}
