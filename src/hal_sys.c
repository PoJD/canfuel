/* hal_sys.c -- clock, ports, A/D and EEPROM on the PIC18F25K80.
 *
 * HARDWARE. Every register name, bit and timing below is quoted from
 * DS39977C (PIC18F66K80 family, which covers the PIC18F25K80). Where the
 * datasheet is deliberately not followed it says so and says why -- there is
 * exactly one such place, in hal_eeprom_write().
 *
 * The pin assignment comes from the board and is frozen; it is reproduced in
 * CLAUDE.md and originates in kicad/canfuel/docs/implementation-plan.md §4.2:
 *
 *   RA0  DBG_EN   jumper JP1 to +5 V, 10 k pull-down     input
 *   RB2  CAN_TX   MCP2562 pin 1                          hal_can.c
 *   RB3  CAN_RX   MCP2562 pin 4                          hal_can.c
 *   RC0  LED_PWR  1 k to an LED to ground, active high   output
 *   RC1  LED_CAN  1 k to an LED to ground, active high   output
 */
#include "pic_config.h"     /* #pragma config ... and then <xc.h>          */

#include <stdbool.h>
#include <stdint.h>

#include "hal_sys.h"

/* --- the millisecond clock ---------------------------------------------- */

/* Written by the timer interrupt, read by everything else. */
static volatile uint32_t g_millis = 0;

/* Timer2 makes the millisecond, and it makes it exactly.
 *
 * DS39977C §15.1: "TMR2 is incremented from 00h on each clock (FOSC/4)", with
 * a prescaler of 1:1, 1:4 or 1:16 (Register 15-1, T2CKPS<1:0>) and a 1:1..1:16
 * postscaler on the TMR2-to-PR2 match (T2OUTPS<3:0>). §15.0: the match "resets
 * the value of TMR2 to 00h on the next cycle", so a period register of N gives
 * N+1 counts.
 *
 * FOSC/4 is 4 MHz -- DS39977C, CLKOUT in the pin table: "OSC2 pin outputs
 * CLKO, which has 1/4 the frequency of OSC1 and denotes the instruction cycle
 * rate" -- so one timer clock is 250 ns.
 *
 *   250 ns x prescale 4          = 1 us per count
 *   1 us   x (PR2 + 1) = 250     = 250 us per match
 *   250 us x postscale 4         = 1000 us per interrupt
 *
 * No remainder, no reload, nothing to drift. Timer0 would need a reload every
 * interrupt and would drift by the latency of each one; that is why the
 * sibling projects' Timer0 heartbeat was not copied.
 *
 * T2CON = 0 0011 1 01: T2OUTPS<3:0> = 0011 (1:4), TMR2ON = 1,
 * T2CKPS<1:0> = 01 (1:4). */
#define T2CON_1MS       0x1Du
#define PR2_1MS         249u

/* --- the A/D, and what VddConv is honestly worth ------------------------ */

/* The plan is to measure the internal band gap against VDD and invert:
 * the converter's reference is AVDD, the input is channel 31, so
 *
 *   code = 4096 x VBG / VDD    =>    VDD = VBG x 4096 / code
 *
 * DS39977C Register 23-1: "11111 = Channel 31 (1.024V band gap)", and
 * Table 31-25 parameter A01: resolution is 12 bits, which is where the 4096
 * comes from. In 0.01 V that is 100 x 1.024 x 4096 / code = 419430 / code.
 *
 * Two honest caveats, both of them the datasheet's:
 *
 * - 1.024 V appears in DS39977C only in the channel list. There is no
 *   tolerance, no min and no max anywhere in Section 31.0 for it, so the
 *   nominal arithmetic above cannot be an absolute reading and was 4.1 % out
 *   on the one board measured. VDD_CAL_* in config.h is the per-unit
 *   calibration that closes that, and it is a measurement against a meter
 *   rather than a specification: only as good as the meter, and only true for
 *   the board it was taken on. A part with no calibration of its own is still
 *   a trend and a sanity check.
 * - Table 31-25 specifies the 12-bit resolution only for VREF >= 3.0 V, and
 *   VREF here is VDD. Below 3 V the number stops meaning anything -- which is
 *   also why the brown-out trip point in pic_config.h is 3.0 V.
 */
/* VDD_NUMERATOR_C is in config.h with the recipe that produced it. It is this
 * unit's, measured against a meter, and it is the only calibration this
 * reading can have. */

/* Anything above this is not a supply voltage, it is a broken conversion.
 * The MCP2562 and the K80 are both 5 V parts; 20 V is well past absurd. */
#define VDD_MAX_C       2000u

/* ADCON0: CHS<4:0> = 11111 (band gap) in bits 6-2, ADON in bit 0.
 * ADCON2: ADFM = 1 (right justified), ACQT<2:0> = 100 (8 TAD),
 *         ADCS<2:0> = 101 (FOSC/16).
 *
 * TAD = 16 TOSC = 1 us at 16 MHz. Table 23-1 allows 16 TOSC up to a 20 MHz
 * device clock, and Table 31-26 parameter 130 requires 0.8 us <= TAD <=
 * 12.5 us. 8 TAD of acquisition is 8 us against the 2.45 us that Equation 23-3
 * works out for the worst case and the 1.4 us of parameter 135. */
#define ADCON0_VBG      0x7Du
#define ADCON2_CFG      0xA5u

/* --- ports -------------------------------------------------------------- */

/* DS39977C §2.7: "Unused I/O pins should be configured as outputs and driven
 * to a logic low state. Alternatively, connect a 1 k to 10 k resistor to VSS
 * on unused pins and drive the output to logic low."
 *
 * There are no such resistors on this board -- fourteen of them would have
 * cost more area than they were worth, and the escape header that used to
 * break these pins out was removed to make the LEDs and the ICSP connector
 * routable. So the first option is the only one available, and this is the
 * only thing standing between fourteen pins and floating inputs.
 *
 * TRISA = 0000 0001  RA0 in (DBG_EN); RA1, RA2, RA3, RA5 out low.
 *                    RA6/RA7 are OSC2/OSC1 in HS mode and TRIS does not apply.
 *                    The 28-pin part has no RA4: pin 6 is VDDCORE/VCAP.
 * TRISB = 1100 1000  RB3 in (CANRX, required); RB2 out (CANTX);
 *                    RB0, RB1, RB4, RB5 out low;
 *                    RB6/RB7 left as inputs -- they are PGC/PGD on the ICSP
 *                    header, and driving them would fight a PICkit. They are
 *                    not in the fourteen for exactly that reason.
 * TRISC = 0000 0000  RC0/RC1 out (LEDs); RC2-RC7 out low.
 *
 * RB2/RB3 are set here as well as in hal_can_init(): this function writes
 * whole TRIS registers, so it cannot leave them undefined even for the
 * instant before the CAN module is brought up. */
#define TRISA_CFG       0x01u
#define TRISB_CFG       0xC8u
#define TRISC_CFG       0x00u

/* --- initialisation ------------------------------------------------------ */

static void ports_init(void)
{
    /* Latches before direction registers, so no pin is driven to the wrong
     * level for the instruction between the two.
     *
     * LATB IS NOT ZERO. Bit 2 is RB2/CANTX, which drives the MCP2562's TXD,
     * and TXD is active low: holding it low asks the transceiver to hold the
     * bus dominant. DS20005167C §1.5 covers what the transceiver then does --
     * disable the CANH and CANL drivers after tPDT, 1.25 ms typical (Table 1-4
     * parameter 11), "in order to prevent the corruption of data on the CAN
     * bus" -- which is a backstop and not a licence. At 500 kbps 1.25 ms is
     * over six hundred bit times, and this runs at every power-up, several
     * milliseconds before hal_can_init() gets to the module. Recessive is
     * idle. */
    LATA = 0x00u;
    LATB = 0x04u;   /* RB2/CANTX recessive; everything else low */
    LATC = 0x00u;

    /* DS39977C §23.6: "As a rule, I/O pins that are multiplexed with analog
     * inputs default to analog operation on any device Reset", and Register
     * 23-8: an ANSELx bit set means "digital input disabled and any inputs
     * read as `0'". RA0 is AN0, so left alone the DBG_EN jumper would read as
     * a permanent zero and the LEDs would simply never work -- a bug that
     * looks exactly like a wiring fault. Clearing both registers makes every
     * analog-capable pin digital, which is what all of them are here. */
    ANCON0 = 0x00u;
    ANCON1 = 0x00u;

    TRISA = TRISA_CFG;
    TRISB = TRISB_CFG;
    TRISC = TRISC_CFG;
}

static void clock_init(void)
{
    /* DS39977C Register 3-1, SCS<1:0>: "00 = Default primary oscillator
     * (OSC1/OSC2 ...). Defined by the FOSC<3:0> Configuration bits". That is
     * the 16 MHz crystal, HS1, no PLL. Everything else in OSCCON concerns the
     * internal oscillators, which are unused. */
    OSCCON = 0x00u;
}

static void timer_init(void)
{
    PR2 = PR2_1MS;
    T2CON = T2CON_1MS;

    /* DS39977C §15.2: the match flag is TMR2IF (PIR1<1>) and the enable is
     * TMR2IE (PIE1<1>). */
    PIR1bits.TMR2IF = 0;
    PIE1bits.TMR2IE = 1;
}

static void interrupts_init(void)
{
    /* One interrupt source, so there is nothing to prioritise. With IPEN = 0
     * every enabled interrupt vectors to the single high-priority vector,
     * which is where XC8 puts __interrupt() with no argument. */
    RCONbits.IPEN = 0;
    INTCONbits.PEIE = 1;
    INTCONbits.GIE = 1;
}

static void adc_init(void)
{
    /* ADCON1 = 0: VCFG<1:0> = 00 selects AVDD as VREF+, VNCFG = 0 selects
     * AVSS as VREF-, CHSN<2:0> = 000 selects AVSS as the negative input.
     * Measuring the band gap against the supply is the whole point. */
    ADCON1 = 0x00u;
    ADCON2 = ADCON2_CFG;
    ADCON0 = ADCON0_VBG;    /* also turns the module on */

    /* DS39977C Table 31-11 parameter 36, TIVRST: the internal reference takes
     * 25 us typ to become stable. Wait for it once here rather than before
     * every conversion. */
    __delay_us(50);
}

/* Latched by reset_cause_init() before anything can disturb it, and handed to
 * the 0x603 diagnostic frame. */
static uint8_t g_reset_cause = 0u;

/* Why did the part start? DS39977C Register 5-1, and every flag in it is
 * **active low** -- a zero means the event happened, which is the opposite of
 * the way it reads.
 *
 *   POR  bit 1   0 = a Power-on Reset occurred
 *   BOR  bit 0   0 = a Brown-out Reset occurred
 *   TO   bit 3   0 = a WDT time-out occurred          (read-only)
 *   RI   bit 4   0 = a RESET instruction was executed
 *
 * The stack bits are elsewhere: STKPTR's STKFUL and STKOVF, which are active
 * high and which STVREN = ON turns into a reset (pic_config.h).
 *
 * This is worth more than everything else in the frame put together on a
 * device behind a dashboard. A converter that quietly restarts every few
 * minutes looks, from the display, exactly like one that is working -- the
 * accumulators come back out of the EEPROM and the numbers are plausible. The
 * uptime beside this byte is what makes it visible, and this byte is what says
 * whether it was the watchdog (a hang) or the brown-out detector (the car's
 * supply), which are different faults with different fixes.
 *
 * Each flag is written back to its inactive state afterwards, or every reset
 * from here on would still be reporting the power-on that started the day. */
static void reset_cause_init(void)
{
    if (!RCONbits.POR) {
        g_reset_cause |= RESET_CAUSE_POWER_ON;
        RCONbits.POR = 1;
    }
    if (!RCONbits.BOR) {
        g_reset_cause |= RESET_CAUSE_BROWN_OUT;
        RCONbits.BOR = 1;
    }
    if (!RCONbits.TO) {
        /* TO is read-only and is set again by CLRWDT, which the main loop
         * executes on its first pass -- so there is nothing to write back. */
        g_reset_cause |= RESET_CAUSE_WATCHDOG;
    }
    if (!RCONbits.RI) {
        g_reset_cause |= RESET_CAUSE_RESET_INSTR;
        RCONbits.RI = 1;
    }
    if (STKPTRbits.STKFUL || STKPTRbits.STKUNF) {
        g_reset_cause |= RESET_CAUSE_STACK;
        STKPTRbits.STKFUL = 0;
        STKPTRbits.STKUNF = 0;
    }
}

uint8_t hal_sys_reset_cause(void)
{
    return g_reset_cause;
}

void hal_sys_init(void)
{
    reset_cause_init();
    clock_init();
    ports_init();
    adc_init();
    timer_init();
    interrupts_init();
}

/* --- the interrupt ------------------------------------------------------- */

/* The only interrupt in the firmware. CAN is polled, which is what keeps this
 * short enough that a 1 ms period is not a burden at 4 MIPS.
 *
 * XC8 spelled this `void interrupt f(void)' up to v1.4x and
 * `void __interrupt() f(void)' from v2 on, which is what v4 still uses. The
 * sibling projects were built with 1.45; this one is built with v4.
 *
 * The first branch is `make check-hal', where gcc compiles this file against
 * test/xc8stub/xc.h and no such qualifier exists at all.
 *
 * The last branch is deliberately an error rather than a bare function.
 * Getting this qualifier silently dropped on a real build would compile
 * cleanly and produce a device whose millisecond clock never advances --
 * every accumulator frozen, and nothing to point at. Fail at the compiler
 * instead. */
#if defined(CANFUEL_XC8_STUB)
void hal_sys_isr(void)
#elif defined(__XC8_VERSION) && (__XC8_VERSION >= 2000)
void __interrupt() hal_sys_isr(void)
#elif defined(__XC8) || defined(__PICC18__) || defined(HI_TECH_C)
void interrupt hal_sys_isr(void)
#else
#error "Unrecognised compiler: the interrupt qualifier is not optional here."
#endif
{
    if (PIE1bits.TMR2IE && PIR1bits.TMR2IF) {
        g_millis++;
        PIR1bits.TMR2IF = 0;
    }
}

/* --- the clock ----------------------------------------------------------- */

uint32_t hal_sys_millis(void)
{
    uint32_t now;
    uint8_t  gie;

    /* Four bytes on an eight-bit machine: the interrupt can land between two
     * of them and hand back a value that was never on the clock. Bracket the
     * read, and restore GIE rather than forcing it on -- this is also called
     * from inside the EEPROM write path. */
    gie = (uint8_t)INTCONbits.GIE;
    INTCONbits.GIE = 0;
    now = g_millis;
    if (gie) {
        INTCONbits.GIE = 1;
    }

    return now;
}

/* --- supply voltage ------------------------------------------------------ */

/* The filtered supply, at 1/32 of a hundredth of a volt. Zero means nothing
 * has been converted yet, which is why the first sample seeds it outright. */
static uint16_t g_vdd_q5 = 0u;

uint16_t hal_sys_vdd_c(void)
{
    uint16_t target_q5;
    uint16_t code;
    uint32_t vdd_c;

    /* DS39977C §23.7: "The GO/DONE bit should NOT be set in the same
     * instruction that turns on the A/D." ADON has been set since adc_init(),
     * so there is nothing to wait for here. */
    ADCON0bits.GO = 1;
    while (ADCON0bits.GO) {
        /* 14 TAD per 12-bit conversion plus 8 TAD of acquisition, so about
         * 22 us. Not worth an interrupt. */
    }

    /* ADFM = 1, so the 12-bit result is right justified across the pair. */
    code = (uint16_t)(((uint16_t)ADRESH << 8) | ADRESL);
    code &= 0x0FFFu;

    if (code == 0u) {
        return 0u;      /* nothing connected to the reference; say so */
    }

    vdd_c = (VDD_NUMERATOR_C + (code / 2u)) / code;
    if (vdd_c > VDD_MAX_C) {
        vdd_c = VDD_MAX_C;
    }

    /* Filtered, and config.h says why: one conversion carries several times an
     * LSB of scatter, so the raw value would walk the display's last digit
     * around ten times a second. Seeded from the first conversion rather than
     * ramped up from zero -- the very first frame after a reset should carry a
     * supply voltage, not a fifth of one.
     *
     * SIXTEEN BITS AND NOT THIRTY-TWO. vdd_c is clamped to VDD_MAX_C = 2000
     * just above, so the value at 1/32 of a hundredth of a volt has a ceiling
     * of 64,000 and a uint16 holds it with room. The 32-bit version of exactly
     * this cost 518 bytes of program memory, because a shift of four is a
     * rotate loop and doing it over four bytes is four times the loop --
     * docs/optimisation.md, the narrowest type that provably holds the value.
     * What Q5 costs is a dead band: a difference under 16/32 of a hundredth of
     * a volt moves nothing, which is half the resolution of the field. */
    target_q5 = (uint16_t)(vdd_c << 5);
    if (g_vdd_q5 == 0u) {
        g_vdd_q5 = target_q5;
    } else if (target_q5 > g_vdd_q5) {
        g_vdd_q5 = (uint16_t)(g_vdd_q5
                              + ((target_q5 - g_vdd_q5) >> VDD_FILTER_SHIFT));
    } else {
        g_vdd_q5 = (uint16_t)(g_vdd_q5
                              - ((g_vdd_q5 - target_q5) >> VDD_FILTER_SHIFT));
    }

    return (uint16_t)((g_vdd_q5 + 16u) >> 5);
}

/* --- jumper and LEDs ----------------------------------------------------- */

bool hal_sys_debug_enabled(void)
{
    /* JP1 pulls RA0 to +5 V; a 10 k resistor pulls it down. An absent jumper
     * is therefore a defined low, not a floating input. RA0 was switched to
     * digital in ports_init(). */
    return PORTAbits.RA0 ? true : false;
}

void hal_sys_led_pwr(bool on)
{
    LATCbits.LATC0 = (on && hal_sys_debug_enabled()) ? 1 : 0;
}

void hal_sys_led_can(bool on)
{
    LATCbits.LATC1 = (on && hal_sys_debug_enabled()) ? 1 : 0;
}

void hal_sys_watchdog_clear(void)
{
    CLRWDT();
}

/* --- EEPROM -------------------------------------------------------------- */

/* 1,024 bytes on the PIC18F25K80 (DS39977C device summary table). persist.c
 * uses 0..767 as 64 slots of 12 bytes and leaves the top 256 alone.
 *
 * The address is EEADRH:EEADR, ten bits wide (DS39977C §8.0). */
static void eeprom_address(uint16_t addr)
{
    EEADRH = (uint8_t)((addr >> 8) & 0x03u);
    EEADR  = (uint8_t)(addr & 0xFFu);
}

uint8_t hal_eeprom_read(uint16_t addr, void *ctx)
{
    (void)ctx;

    /* DS39977C Example 8-1, in order: address, EEPGD = 0 (data EEPROM rather
     * than program memory), CFGS = 0 (memory rather than the Configuration
     * registers), RD = 1, one NOP, then read. §8.3: "The data is available
     * after one instruction cycle, in the EEDATA register. It can be read
     * after one NOP instruction." */
    eeprom_address(addr);
    EECON1bits.EEPGD = 0;
    EECON1bits.CFGS  = 0;
    EECON1bits.RD    = 1;
    NOP();

    return EEDATA;
}

void hal_eeprom_write(uint16_t addr, uint8_t value, void *ctx)
{
    uint8_t gie;

    (void)ctx;

    eeprom_address(addr);
    EEDATA = value;
    EECON1bits.EEPGD = 0;
    EECON1bits.CFGS  = 0;

    /* DS39977C §8.4: "The WREN bit must be set on a previous instruction. Both
     * WR and WREN cannot be set with the same instruction." */
    EECON1bits.WREN = 1;

    /* DS39977C Example 8-2 marks this the Required Sequence, and §8.4 is
     * explicit that "the write will not begin if this sequence is not exactly
     * followed (write 55h to EECON2, write 0AAh to EECON2, then set WR bit)".
     * An interrupt landing between the 0x55 and the 0xAA aborts the unlock and
     * the write fails silently, which is why the bracket is not optional here
     * the way it arguably is in a switch that sleeps most of the time.
     * (piclib/dao.c does have it, as di()/ei() around the whole operation.) */
    gie = (uint8_t)INTCONbits.GIE;
    INTCONbits.GIE = 0;
    EECON2 = 0x55u;
    EECON2 = 0xAAu;
    EECON1bits.WR = 1;

    /* DELIBERATE DEVIATION from Example 8-2, which keeps GIE clear until after
     * the WR poll. We restore it the instant WR is set instead.
     *
     * Why: a byte write takes 4 ms typical (Table 31-1, D122) and persist.c
     * writes a 12-byte record, so following the example literally would hold
     * interrupts off for about 48 ms three times a minute. The only interrupt in
     * firmware is the millisecond clock, and that clock is what every
     * accumulator in the core is integrated against -- losing 48 ms of it per
     * minute is an 0.08 % error in distance and in the trip average, silently.
     *
     * Why it is safe: the Required Sequence is over. §8.4: "After a write
     * sequence has been initiated, EECON1, EEADRH:EEADR and EEDATA cannot be
     * modified", so nothing an interrupt could do disturbs the cycle in
     * flight. What the datasheet asks for is that the unlock not be
     * interrupted, and it is not. */
    if (gie) {
        INTCONbits.GIE = 1;
    }

    /* §8.4: "At the completion of the write cycle, the WR bit is cleared in
     * hardware".
     *
     * The watchdog is deliberately NOT cleared inside this loop. If WR never
     * clears, the hardware is broken and a reset is the correct outcome; a
     * CLRWDT() here would turn that into a permanent hang. 48 ms of writing
     * against a 2.048 s watchdog leaves the margin to afford this. */
    while (EECON1bits.WR) {
        /* wait */
    }

    /* §8.4: "the EEPROM Interrupt Flag bit (EEIF) is set. The user may either
     * enable this interrupt or poll this bit; EEIF must be cleared by
     * software." It is PIR4<6> (Register 10-x). Nothing enables it; it still
     * has to be cleared. */
    PIR4bits.EEIF = 0;

    /* §8.4: "The WREN bit should be kept clear at all times, except when
     * updating the EEPROM. The WREN bit is not cleared by hardware." */
    EECON1bits.WREN = 0;

    /* WRERR IS DELIBERATELY NOT READ, and this is a decision rather than an
     * oversight. Register 8-1 defines it as "a write operation is prematurely
     * terminated (any Reset during self-timed programming...)", and §7.5.3
     * says such a location "should be verified and reprogrammed if needed".
     *
     * We do neither, because persist.c already covers it and covers it better.
     * The failure this guards against is losing power mid-write -- the
     * ignition going off during the 48 ms every twenty seconds, which is
     * about one switch-off in four hundred. When it happens the CPU is not running to read
     * WRERR anyway; on the next start persist_load() finds that slot's CRC
     * does not match and skips it, and the ring means the record it skips is
     * the OLDEST of sixty-four rather than the newest. Reprogramming the
     * location would be pointless as well: the next write goes to the next
     * slot regardless. So the bit would tell us only what the CRC already
     * does, one boot later, and nothing would be done differently. */
}

const persist_backend_t hal_eeprom_backend = {
    hal_eeprom_read,
    hal_eeprom_write,
    (void *)0
};
