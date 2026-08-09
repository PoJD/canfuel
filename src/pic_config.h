/* pic_config.h -- the PIC18F25K80 configuration bits, and nothing else.
 *
 * HARDWARE. Included by main.c only, and it must be included before <xc.h>
 * reaches anything else, which is why it includes <xc.h> itself at the end --
 * the same shape as CanSwitch.X/config.h in the sibling `can` repo.
 *
 * Every bit below is either quoted from DS39977C or marked as inherited from
 * the sibling projects. The starting point was CanSwitch.X/config.h, a working
 * configuration for the same PIC18F25K80 at the same 16 MHz crystal; the table
 * in CLAUDE.md lists what changed and why. In short: CANMX, SOSCSEL is now
 * load-bearing rather than incidental, the watchdog goes on, and the brown-out
 * trip point moves from 1.8 V to 3.0 V.
 *
 * Do not rename this file to config.h. That name is taken by the pure core's
 * constants header, which must never see <xc.h>.
 */
#ifndef PIC_CONFIG_H
#define PIC_CONFIG_H

/* --- CONFIG1L ----------------------------------------------------------- */

/* We never sleep, so the ultra low-power regulator has nothing to do.
 * DS39977C Register 28-1: RETEN `1' = ultra low-power regulator is disabled,
 * `0' = enabled -- the polarity is inverted against the name, and XC8's
 * keyword follows the meaning rather than the bit, so OFF is the `1'. */
#pragma config RETEN = OFF

/* Only matters in Sleep. Inherited from CanSwitch.X. */
#pragma config INTOSCSEL = LOW

/* LOAD-BEARING, and the easiest bit on this board to get wrong.
 *
 * DS39977C Register 28-1, SOSCSEL<1:0>:
 *   10 = Digital (SCLKI) mode; I/O port functionality of RC0 and RC1 is enabled
 *
 * Pins 11 and 12 of the 28-pin part are RC0/SOSCO/SCLKI and RC1/SOSCI
 * (DS39977C pin table). Both LEDs hang off exactly those two pins, so without
 * DIG they belong to the secondary oscillator and never light. That failure
 * looks precisely like a dry joint on the LEDs. */
#pragma config SOSCSEL = DIG

/* XC8 requires the extended instruction set to be off. */
#pragma config XINST = OFF

/* --- CONFIG1H ----------------------------------------------------------- */

/* 16 MHz crystal. DS39977C Register 28-2: `0011 = HS1, HS oscillator (medium
 * power, 4 MHz-16 MHz)' and `0010 = HS2 ... (high power, 16 MHz-25 MHz)'.
 * 16 MHz is the top of one range and the bottom of the other, so either is
 * defensible; HS1 is what both sibling projects run at this crystal.
 *
 * Table 3-1 of the datasheet appears to contradict this -- its frequency
 * column is misaligned against its mode column by one row from HS1 downwards.
 * Register 28-2 is the one to believe. */
#pragma config FOSC = HS1

/* No PLL: FOSC is 16 MHz and the instruction clock is FOSC/4 = 4 MHz. Both
 * the millisecond timer and the CAN bit rate are computed from that. */
#pragma config PLLCFG = OFF

/* Nothing to fail over to and nothing to switch over from -- there is exactly
 * one oscillator on this board. Inherited from CanSwitch.X. */
#pragma config FCMEN = OFF
#pragma config IESO = OFF

/* --- CONFIG2L ----------------------------------------------------------- */

/* DS39977C Table 31-11 parameter 33: the power-up timer holds reset for
 * 65.5 ms typ. Cheap insurance in a car, where the 5 V rail comes up with the
 * ignition rather than from a bench supply. */
#pragma config PWRTEN = ON

/* Brown-out reset enabled in hardware. CanSwitch.X uses NOSLP, which only
 * differs in Sleep, and we never sleep. */
#pragma config BOREN = ON
#pragma config BORPWR = ZPBORMV

/* CHANGED from CanSwitch.X, which trips at 1.8 V.
 *
 * DS39977C Register 28-3: BORV<1:0> `00' = BVDD is set to 3.0V. We take that
 * one because of the A/D, not because of the CPU: Table 31-25 parameters A01
 * and A50 specify 12-bit resolution only for VREF >= 3.0 V, and VREF here is
 * VDD itself. Below 3 V the converter would keep running and keep sending
 * numbers that are no longer specified -- worse than resetting. */
#pragma config BORV = 0

/* --- CONFIG2H ----------------------------------------------------------- */

/* CHANGED from both sibling projects, which run with the watchdog off.
 *
 * A light switch wedged in a wall gets noticed and power-cycled. A converter
 * wedged behind an air vent does not, and it feeds a display the driver is
 * reading. DS39977C Register 28-4: `11 = WDT is enabled in hardware'.
 *
 * DS39977C §28.2: the WDT period is 4 ms nominal, multiplied by the
 * postscaler; `01001 = 1:512 (2.048s)'. The longest the main loop can go
 * without clearing the watchdog is one EEPROM record -- 12 bytes at 4 ms
 * typical each (Table 31-1 D122), about 48 ms, once a minute. Two seconds is
 * forty times that, so a real hang is the only thing that can trip it. */
#pragma config WDTEN = ON
#pragma config WDTPS = 512

/* --- CONFIG3H ----------------------------------------------------------- */

/* THE bit to get right on this board.
 *
 * DS39977C Register 28-5, CONFIG3H<0>:
 *   1 = CANTX and CANRX pins are located on RB2 and RB3, respectively
 *   0 = CANTX and CANRX pins are located on RC6 and RC7, respectively
 *
 * The board is wired RB2/RB3, so the bit is set. Note that §27.1's prose says
 * the opposite -- that the pins "can be placed on alternate I/O pins by
 * setting the CANMX Configuration bit" -- and it is simply wrong. The register
 * table, the pin-table footnote and CanSwitch.X's own comment on PORTC all
 * agree against it.
 *
 * CanSwitch.X sets PORTC. Copying that file wholesale is the single most
 * expensive mistake available here: the escape header that used to break out
 * RC6/RC7 was removed from the board, so fixing it afterwards means soldering
 * to the underside of the PDIP socket. */
#pragma config CANMX = PORTB

#pragma config MSSPMSK = MSK7
#pragma config MCLRE = ON

/* T3CKMX and T0CKMX are deliberately not set. DS39977C Register 28-5, note 1:
 * they are "implemented only on the 64-pin devices ... Maintain as `0' on
 * 28-pin, 40-pin and 44-pin devices", and both default to `1'. On this part
 * they do nothing at all, and the XC8 keyword for the `0' state could not be
 * verified against a device header from here, so a guess would be worse than
 * the documented default. Neither sibling project sets them either. */

/* --- CONFIG4L ----------------------------------------------------------- */

/* Stack overflow and underflow reset the device rather than corrupting it
 * silently. Inherited from CanSwitch.X. */
#pragma config STVREN = ON
#pragma config BBSIZ = BB2K

/* --- CONFIG5-7: no code or table protection ----------------------------- */

#pragma config CP0 = OFF
#pragma config CP1 = OFF
#pragma config CP2 = OFF
#pragma config CP3 = OFF
#pragma config CPB = OFF
#pragma config CPD = OFF
#pragma config WRT0 = OFF
#pragma config WRT1 = OFF
#pragma config WRT2 = OFF
#pragma config WRT3 = OFF
#pragma config WRTC = OFF
#pragma config WRTB = OFF
#pragma config WRTD = OFF
#pragma config EBTR0 = OFF
#pragma config EBTR1 = OFF
#pragma config EBTR2 = OFF
#pragma config EBTR3 = OFF
#pragma config EBTRB = OFF

/* The crystal, for XC8's __delay_us()/__delay_ms(). This is the oscillator
 * frequency, not the instruction rate. */
#define _XTAL_FREQ 16000000UL

#include <xc.h>

#endif /* PIC_CONFIG_H */
