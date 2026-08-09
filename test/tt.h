/* tt.h -- a test framework small enough to read in one sitting.
 *
 * Header only, so the Makefile rule that compiles one test_*.c against the
 * core sources does not have to grow a list of helper objects.
 *
 *      static void test_something(void) { TT_EQ(2 + 2, 4); }
 *      int main(void) { TT_RUN(test_something); return TT_SUMMARY(); }
 *
 * Every check keeps running after a failure -- one run should report every
 * broken expectation, not just the first.
 */
#ifndef TT_H
#define TT_H

#include <stdio.h>

static int tt_failures = 0;
static int tt_checks = 0;

#define TT_FAIL(...)                                                    \
    do {                                                                \
        tt_failures++;                                                  \
        printf("\n      FAIL  %s:%d: ", __FILE__, __LINE__);            \
        printf(__VA_ARGS__);                                            \
        printf("\n");                                                   \
    } while (0)

#define TT_TRUE(cond)                                                   \
    do {                                                                \
        tt_checks++;                                                    \
        if (!(cond)) {                                                  \
            TT_FAIL("expected true: %s", #cond);                        \
        }                                                               \
    } while (0)

#define TT_FALSE(cond)                                                  \
    do {                                                                \
        tt_checks++;                                                    \
        if (cond) {                                                     \
            TT_FAIL("expected false: %s", #cond);                       \
        }                                                               \
    } while (0)

/* Everything the core produces is an integer, so one comparison covers it. */
#define TT_EQ(actual, expected)                                         \
    do {                                                                \
        long long tt_a = (long long)(actual);                           \
        long long tt_e = (long long)(expected);                         \
        tt_checks++;                                                    \
        if (tt_a != tt_e) {                                             \
            TT_FAIL("%s: expected %lld, got %lld", #actual, tt_e, tt_a); \
        }                                                               \
    } while (0)

#define TT_NEAR(actual, expected, tol)                                  \
    do {                                                                \
        long long tt_a = (long long)(actual);                           \
        long long tt_e = (long long)(expected);                         \
        long long tt_d = tt_a > tt_e ? tt_a - tt_e : tt_e - tt_a;       \
        tt_checks++;                                                    \
        if (tt_d > (long long)(tol)) {                                  \
            TT_FAIL("%s: expected %lld +/- %lld, got %lld",             \
                    #actual, tt_e, (long long)(tol), tt_a);             \
        }                                                               \
    } while (0)

#define TT_RANGE(actual, lo, hi)                                        \
    do {                                                                \
        long long tt_a = (long long)(actual);                           \
        tt_checks++;                                                    \
        if (tt_a < (long long)(lo) || tt_a > (long long)(hi)) {          \
            TT_FAIL("%s: expected %lld..%lld, got %lld", #actual,       \
                    (long long)(lo), (long long)(hi), tt_a);            \
        }                                                               \
    } while (0)

#define TT_RUN(fn)                                                      \
    do {                                                                \
        int tt_before = tt_failures;                                    \
        printf("  %-52s", #fn);                                         \
        fflush(stdout);                                                 \
        fn();                                                           \
        printf("%s\n", tt_failures == tt_before ? "ok" : "  ^ failed"); \
    } while (0)

#define TT_SUMMARY()                                                    \
    (printf("  %d checks, %d failed\n", tt_checks, tt_failures),        \
     tt_failures == 0 ? 0 : 1)

#endif /* TT_H */
