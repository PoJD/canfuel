/* test_divconst.c -- the reciprocal division in src/divconst.h really divides.
 *
 * This is the test the optimisation was made conditional on. A magic number
 * that is one out on a value the fixtures never produce would put a wrong
 * number on the display and break nothing else, so "the other tests still
 * pass" is not evidence here.
 *
 * tools/divconst.py proves each (magic, shift) pair mathematically, over the
 * range declared for it, using the Granlund-Montgomery condition. What THIS
 * proves is different and complementary: that the C in divconst.h -- sixteen
 * byte products assembled by hand -- actually computes that product. A proof
 * about arithmetic says nothing about whether the code implements it.
 *
 *   make -C test test
 *       the sampled run: 1.17 million checks, part of the normal suite.
 *
 *   gcc -O2 -DEXHAUSTIVE -I../src -I. -o exh test_divconst.c ../src/decode.c \n *       ../src/compute.c ../src/txframes.c ../src/persist.c && ./exh
 *       every 32-bit value against every divisor. Tens of minutes, so it is
 *       not wired into `make test` -- it is what you run once when a magic
 *       number changes, and it was run when these were introduced.
 */

#include "divconst.h"
#include "tt.h"

/* Every divisor in divconst.h, with the range divconst.py declares for it. */
/* The table walks the divisors at run time, so it uses the three-argument
 * div_const_() rather than the two-argument div_const() the firmware calls.
 * They are the same expression; only the firmware's form has the shift as a
 * literal, which is what keeps it out of a shift loop on the PIC. */
struct divisor {
    const char *name;
    uint32_t d;
    uint32_t magic;
    uint8_t  shift;
    uint32_t limit;         /* exclusive; 0 means the whole 32-bit range */
};

static const struct divisor DIVISORS[] = {
    { "10",    10u,    DIVC_10,    0u },
    { "100",   100u,   DIVC_100,   0u },
    { "120",   120u,   DIVC_120,   0u },
    { "1000",  1000u,  DIVC_1000,  0u },
    { "3600",  3600u,  DIVC_3600,  0u },
    { "10000", 10000u, DIVC_10000, 0u },
    { "95500", 95500u, DIVC_95500, 1073741824ul },   /* 2**30, see divconst.py */
};

#define N_DIVISORS  (sizeof DIVISORS / sizeof DIVISORS[0])

static uint32_t top_of(const struct divisor *dv)
{
    return dv->limit ? dv->limit - 1u : 0xFFFFFFFFul;
}

/* The values that can break a reciprocal: either side of a multiple of d, and
 * the ends of the range. Everything between two multiples has the same
 * quotient, so if the boundaries are right the interior cannot be wrong. */
static void test_boundaries_around_every_multiple(void)
{
    size_t i;
    for (i = 0; i < N_DIVISORS; i++) {
        const struct divisor *dv = &DIVISORS[i];
        uint32_t top = top_of(dv);
        uint32_t k;

        TT_EQ(div_const_(0u, dv->magic, dv->shift), 0u);
        TT_EQ(div_const_(top, dv->magic, dv->shift), top / dv->d);
        TT_EQ(div_const_(top - 1u, dv->magic, dv->shift), (top - 1u) / dv->d);

        /* The first 50,000 multiples, and both sides of each. */
        for (k = 1; k < 50000u; k++) {
            uint32_t x = k * dv->d;
            if (x > top) {
                break;
            }
            TT_EQ(div_const_(x, dv->magic, dv->shift), k);
            TT_EQ(div_const_(x - 1u, dv->magic, dv->shift), k - 1u);
        }

        /* And the last few, where a 33-bit magic would have gone wrong. */
        for (k = top / dv->d; k > 0u && k > top / dv->d - 5000u; k--) {
            uint32_t x = k * dv->d;
            TT_EQ(div_const_(x, dv->magic, dv->shift), k);
            TT_EQ(div_const_(x - 1u, dv->magic, dv->shift), k - 1u);
        }
    }
}

/* A cheap deterministic spread across the whole range, so nothing depends on
 * the boundaries being the only interesting values. */
static void test_a_spread_of_ordinary_values(void)
{
    size_t i;
    uint32_t seed = 0x12345678ul;
    uint32_t n;

    for (n = 0; n < 40000u; n++) {
        /* xorshift32: no library, same sequence everywhere. */
        seed ^= seed << 13;
        seed ^= seed >> 17;
        seed ^= seed << 5;
        for (i = 0; i < N_DIVISORS; i++) {
            const struct divisor *dv = &DIVISORS[i];
            uint32_t x = dv->limit ? seed % dv->limit : seed;
            TT_EQ(div_const_(x, dv->magic, dv->shift), x / dv->d);
        }
    }
}

/* The rounding wrapper, which is what the core actually calls. */
static void test_the_rounding_form(void)
{
    size_t i;
    for (i = 0; i < N_DIVISORS; i++) {
        const struct divisor *dv = &DIVISORS[i];
        uint32_t half = dv->d / 2u;
        uint32_t k;
        for (k = 0; k < 20000u; k++) {
            uint32_t x = k * 7919u;                  /* a prime, to skip about */
            if (dv->limit && x + half >= dv->limit) {
                break;
            }
            TT_EQ(div_const_round_(x, half, dv->magic, dv->shift),
                  (x + half) / dv->d);
        }
    }
}

/* mulhi_u32 on its own, against the 64-bit product the host can do directly.
 * If this is wrong every divisor is wrong, so it is worth isolating. */
static void test_mulhi_against_a_64_bit_product(void)
{
    uint32_t seed = 0xDEADBEEFul;
    uint32_t n;
    for (n = 0; n < 60000u; n++) {
        uint32_t a, b;
        seed ^= seed << 13; seed ^= seed >> 17; seed ^= seed << 5;
        a = seed;
        seed ^= seed << 13; seed ^= seed >> 17; seed ^= seed << 5;
        b = seed;
        TT_EQ(mulhi_u32(a, b), (uint32_t)(((uint64_t)a * b) >> 32));
    }
    TT_EQ(mulhi_u32(0u, 0xFFFFFFFFul), 0u);
    TT_EQ(mulhi_u32(0xFFFFFFFFul, 0xFFFFFFFFul), 0xFFFFFFFEul);
    TT_EQ(mulhi_u32(1u, 0xFFFFFFFFul), 0u);
    TT_EQ(mulhi_u32(0x80000000ul, 0x80000000ul), 0x40000000ul);
}

#ifdef EXHAUSTIVE
/* Every 32-bit value against every divisor. Minutes, not seconds, which is why
 * it is behind a flag -- but it leaves nothing to argue about. */
static void test_every_value_there_is(void)
{
    size_t i;
    for (i = 0; i < N_DIVISORS; i++) {
        const struct divisor *dv = &DIVISORS[i];
        uint32_t top = top_of(dv);
        uint32_t x = 0;
        for (;;) {
            TT_EQ(div_const_(x, dv->magic, dv->shift), x / dv->d);
            if (tt_failures) {
                return;
            }
            if (x == top) {
                break;
            }
            x++;
        }
        TT_TRUE(1);
    }
}
#endif

int main(void)
{
    TT_RUN(test_mulhi_against_a_64_bit_product);
    TT_RUN(test_boundaries_around_every_multiple);
    TT_RUN(test_a_spread_of_ordinary_values);
    TT_RUN(test_the_rounding_form);
#ifdef EXHAUSTIVE
    TT_RUN(test_every_value_there_is);
#endif
    return TT_SUMMARY();
}
