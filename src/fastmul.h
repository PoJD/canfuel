/* fastmul.h -- 32-bit multiplication that uses the hardware multiplier.
 *
 * PURE C, no hardware. Read docs/optimisation.md before changing this.
 *
 * XC8 v4.00 calls ___lmul for any multiply wider than 8 bits, and ___lmul is a
 * loop of one iteration per bit: 849 cycles. The part has a single-cycle 8x8
 * multiplier that the compiler will use for uint8 x uint8 and uint16 x uint8
 * and for nothing else, so the wide product is assembled from byte products
 * here instead.
 *
 * It is a separate header from divconst.h so that decode.c, which needs the
 * multiply and not the division, does not pull in an unused static function --
 * which -Werror=unused-function turns into a build failure.
 */
#ifndef FASTMUL_H
#define FASTMUL_H

#include <stdint.h>

/* The low 32 bits of x * m, for any m that fits 16 bits. Seven byte products.
 *
 * SAME PROBLEM AS THE DIVISION, AND WORSE. XC8 calls ___lmul for any multiply
 * wider than 8 bits, and ___lmul is a per-bit loop costing 849 cycles. After
 * the constant divisions were replaced, it was the largest single item left in
 * the firmware: twelve calls, 10,188 cycles, 2.55 ms -- and mulhi_u32() above
 * costs 300, so a reciprocal division had become nearly three times cheaper
 * than an ordinary multiply sitting next to it.
 *
 * Only the low half is wanted here, and m is at most 16 bits, so the product
 * x_i * m_j is only needed where i + j <= 3. That is seven products rather
 * than the sixteen mulhi_u32 needs: 137 instructions, no branches, no calls.
 *
 * THE CALLER MUST GUARANTEE m FITS 16 BITS. Every use in the core passes
 * either a literal (10, 36, 74, 1000, 3600, 4820) or a value with a bound
 * argued at the call site -- rpm is a uint16 quarter-count divided by four,
 * and dt_ms is gated to 1000 by compute_tick. A caller that passed something
 * wider would silently lose the top bits, which is why this takes a uint16_t
 * and makes the compiler check. */
static uint32_t mul_u32_u16(uint32_t x, uint16_t m)
{
    uint8_t x0 = (uint8_t)x, x1 = (uint8_t)(x >> 8);
    uint8_t x2 = (uint8_t)(x >> 16), x3 = (uint8_t)(x >> 24);
    uint8_t m0 = (uint8_t)m, m1 = (uint8_t)(m >> 8);
    uint32_t acc;

    acc  = (uint32_t)((uint16_t)x0 * m0);
    acc += (uint32_t)((uint16_t)x0 * m1) << 8;
    acc += (uint32_t)((uint16_t)x1 * m0) << 8;
    acc += (uint32_t)((uint16_t)x1 * m1) << 16;
    acc += (uint32_t)((uint16_t)x2 * m0) << 16;
    acc += (uint32_t)((uint16_t)x2 * m1) << 24;
    acc += (uint32_t)((uint16_t)x3 * m0) << 24;
    return acc;
}

#endif /* FASTMUL_H */
