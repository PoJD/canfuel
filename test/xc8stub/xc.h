/* xc.h -- a stub, for gcc, and for one narrow purpose.
 *
 * THIS IS NOT A DEVICE HEADER AND IT PROVES NOTHING ABOUT THE HARDWARE.
 *
 * XC8 is not installed on every machine this repository is worked on, and it
 * is not installed in CI. Without it, hal_can.c, hal_sys.c and main.c would be
 * six hundred lines of C that nothing ever compiles -- and main.c in
 * particular is the one place the pure core's API is actually called, so a
 * wrong argument or a renamed function there would go unnoticed until a device
 * build.
 *
 * So `make check-hal` compiles those three files with gcc -fsyntax-only
 * against this stub. What that catches:
 *
 *   - anything that is not valid C
 *   - calls into decode.h / compute.h / txframes.h / persist.h with the wrong
 *     arguments, the wrong types or the wrong names
 *   - types that do not line up between the HAL headers and their users
 *
 * What it cannot catch, and what only XC8 and a board will:
 *
 *   - a misspelled or non-existent register or bit name. Every name below is
 *     declared here BECAUSE hal_*.c uses it; this file agrees with the code by
 *     construction, not with the silicon.
 *   - anything about widths, addresses, banking or timing
 *
 * Which is exactly why every register in hal_*.c carries a DS39977C citation
 * next to it. The citation is the real check; this is a typo net.
 */
#ifndef CANFUEL_XC8_STUB_H
#define CANFUEL_XC8_STUB_H

#define CANFUEL_XC8_STUB 1

/* --- the two instruction macros XC8 provides ----------------------------- */

#define NOP()           ((void)0)
#define CLRWDT()        ((void)0)
#define __delay_us(x)   ((void)(x))
#define __delay_ms(x)   ((void)(x))

/* --- plain byte-wide special function registers -------------------------- */

#define SFR8(name)      extern volatile unsigned char name

SFR8(LATA);   SFR8(LATB);   SFR8(LATC);
SFR8(TRISA);  SFR8(TRISB);  SFR8(TRISC);
SFR8(ANCON0); SFR8(ANCON1);
SFR8(OSCCON);
SFR8(PR2);    SFR8(T2CON);
SFR8(ADCON0); SFR8(ADCON1); SFR8(ADCON2);
SFR8(ADRESH); SFR8(ADRESL);
SFR8(EEADR);  SFR8(EEADRH); SFR8(EEDATA); SFR8(EECON2);

SFR8(CANCON);  SFR8(CANSTAT); SFR8(ECANCON); SFR8(COMSTAT);
SFR8(BSEL0);
SFR8(BRGCON1); SFR8(BRGCON2); SFR8(BRGCON3); SFR8(CIOCON);
SFR8(RXM0SIDH); SFR8(RXM0SIDL);
SFR8(RXF0SIDH); SFR8(RXF0SIDL);
SFR8(RXF1SIDH); SFR8(RXF1SIDL);
SFR8(RXF2SIDH); SFR8(RXF2SIDL);
SFR8(RXF3SIDH); SFR8(RXF3SIDL);
SFR8(RXF4SIDH); SFR8(RXF4SIDL);
SFR8(RXF5SIDH); SFR8(RXF5SIDL);
SFR8(RXF6SIDH); SFR8(RXF6SIDL);
SFR8(MSEL0);    SFR8(MSEL1);
SFR8(RXFBCON0); SFR8(RXFBCON1); SFR8(RXFBCON2); SFR8(RXFBCON3);
SFR8(RXFCON0);  SFR8(RXFCON1);
SFR8(RXB0CON);  SFR8(RXB1CON);
SFR8(B0CON); SFR8(B1CON); SFR8(B2CON);
SFR8(B3CON); SFR8(B4CON); SFR8(B5CON);
SFR8(RXB0SIDH); SFR8(RXB0SIDL); SFR8(RXB0DLC); SFR8(RXB0D0);
SFR8(RXERRCNT); SFR8(TXERRCNT);

#undef SFR8

/* --- the bit-addressed views, with only the bits hal_*.c names ----------- */

#define SFRBITS(name, fields)                   \
    typedef struct fields name##bits_t;         \
    extern volatile name##bits_t name##bits

SFRBITS(INTCON, { unsigned PEIE : 1; unsigned GIE : 1; });
/* RCON's reset flags are all active low and are read by hal_sys.c to say why
 * the part started. The bit order here is NOT the device's -- see the header
 * comment: this file names what the code names and nothing else. DS39977C
 * Register 5-1 is the real layout. */
SFRBITS(RCON,   { unsigned IPEN : 1; unsigned POR : 1; unsigned BOR : 1;
                  unsigned TO : 1; unsigned RI : 1; });
SFRBITS(STKPTR, { unsigned STKFUL : 1; unsigned STKUNF : 1; });
SFRBITS(PIR1,   { unsigned TMR2IF : 1; });
SFRBITS(PIE1,   { unsigned TMR2IE : 1; });
SFRBITS(PIR4,   { unsigned EEIF : 1; });
SFRBITS(ADCON0, { unsigned GO : 1; });
SFRBITS(PORTA,  { unsigned RA0 : 1; });
SFRBITS(LATB,   { unsigned LATB2 : 1; });
SFRBITS(LATC,   { unsigned LATC0 : 1; unsigned LATC1 : 1; });
SFRBITS(TRISB,  { unsigned TRISB2 : 1; unsigned TRISB3 : 1; });
SFRBITS(EECON1, { unsigned EEPGD : 1; unsigned CFGS : 1; unsigned RD : 1;
                  unsigned WREN : 1; unsigned WR : 1; });
SFRBITS(RXB0CON, { unsigned RXFUL : 1; });
SFRBITS(TXB0CON, { unsigned TXREQ : 1; });
SFRBITS(TXB1CON, { unsigned TXREQ : 1; });
SFRBITS(TXB2CON, { unsigned TXREQ : 1; });

#undef SFRBITS

#endif /* CANFUEL_XC8_STUB_H */
