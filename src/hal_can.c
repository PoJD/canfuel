/* hal_can.c -- ECAN on RB2/RB3 at 500 kbps, Mode 2 (FIFO).
 *
 * HARDWARE. DS39977C calls this chapter 27, not 22 -- the section numbers in
 * older PIC18 CAN datasheets do not carry over.
 *
 * Three decisions shape this file and all three are argued below, at the code
 * they produce: functional Mode 2 rather than Mode 0, polling rather than
 * interrupts, and the access-bank window rather than three copies of the
 * buffer-handling code.
 *
 * THE ACCESS-BANK WINDOW IS A LOADED GUN. In Mode 1 and 2, ECANCON<4:0>
 * decides which CAN buffer the addresses 0F60-0F6Dh -- the ones the header
 * calls RXB0CON..RXB0D7 -- actually refer to (DS39977C Register 27-3). Every
 * function here that touches an RXB0* name sets EWIN first, in the same
 * breath. Anything that forgets would read a message out of an acceptance
 * filter, or write a transmit frame into one.
 */
#include "pic_config.h"     /* #pragma config ... and then <xc.h> */

#include <stdbool.h>
#include <stdint.h>

#include "config.h"
#include "hal_can.h"

/* --- module modes -------------------------------------------------------- */

/* DS39977C Register 27-1, REQOP<2:0>, and Register 27-2, OPMODE<2:0>:
 *
 *   1xx = Configuration    011 = Listen Only    010 = Loopback
 *   001 = Disabled/Sleep   000 = Normal
 *
 * Listen Only and Loopback are not named here because hal_can.h names them:
 * HAL_CAN_MODE_* carry the same codes, so there is one table rather than two
 * that can drift. */
#define MODE_NORMAL         0x00u
#define MODE_CONFIG         0x04u

/* The mode hal_can_init() actually reached, for hal_can_mode(). Not a cache of
 * OPMODE -- it is what the caller asked for and got, which is what an LED
 * should report. */
static hal_can_mode_t g_mode = HAL_CAN_MODE_NORMAL;

/* DS39977C §27.3: "When changing modes, the mode will not actually change
 * until all pending message transmissions are complete. Because of this, the
 * user must verify that the device has actually changed into the requested
 * mode before further operations are executed."
 *
 * The longest wait is one frame in flight, about 230 us at 500 kbps. Each
 * pass of the loop below is a handful of instructions at 4 MIPS, so this
 * bound is tens of milliseconds -- generous, and finite, which is the point.
 * A module that never answers must not be allowed to wedge the firmware. */
#define MODE_TIMEOUT        50000u

/* --- functional mode and the FIFO ---------------------------------------- */

/* MODE 2 RATHER THAN MODE 0, for two independent reasons.
 *
 * Filters. DS39977C §27.4.1: Mode 0 offers "Six acceptance filters, 2 for
 * RXB0 and 4 for RXB1". We need seven identifiers. Mode 1 and 2 offer
 * "Sixteen acceptance filters" that can be pointed at any buffer (§27.4.2,
 * §27.4.3), so each identifier gets its own filter and an exact mask. Squeezing
 * seven identifiers into six Mode 0 filters would mean widening a mask to
 * cover 0x280 and 0x288 together, which lets in whatever else matches.
 *
 * Depth. Mode 0 has two receive buffers. Mode 2 forms a FIFO out of all eight
 * (§27.4.3: "If none of the programmable buffers are configured as a transmit
 * buffer, the FIFO will be 8 buffers deep"). The frames we accept arrive at,
 * per docs/can-decoding.md, 7.5 ms (0x1A0), 10.5 ms (0x280) and 11.8 ms
 * (0x288) for the fast three, plus four slower ones -- call it four frames per
 * 10 ms. Two buffers would be a coin toss; eight is not.
 *
 * ECANCON = 1 0 0 10000: MDSEL<1:0> = 10 (Mode 2), FIFOWM = 0 (unused, we do
 * not take the FIFO interrupt), EWIN<4:0> = 10000 (Receive Buffer 0, which is
 * also the reset value -- leaving EWIN at 00000 here would silently map the
 * acceptance filters over the RXB0 addresses). */
#define ECANCON_MODE2       0x90u

/* EWIN values, DS39977C Register 27-3. FIFO buffer n is EWIN 10000 + n:
 * 10000 = RXB0, 10001 = RXB1, 10010..10111 = B0..B5, in that order, which is
 * exactly the order FP<3:0> counts in. */
#define EWIN_FIFO_BASE      0x10u
#define EWIN_TXB0           0x03u
#define EWIN_TXB1           0x04u
#define EWIN_TXB2           0x05u
#define EWIN_MASK           0x1Fu

/* --- bit timing: 500 kbps out of a 16 MHz crystal ------------------------ */

/* DS39977C Example 27-6: TQ (us) = (2 * (BRP + 1)) / FOSC (MHz).
 * Register 27-52 allows BRP<5:0> = 000000, giving TQ = (2 * 1) / 16 =
 * 0.125 us. Sixteen of those is a 2 us bit time, which is 500 kbps exactly --
 * no remainder and nothing to round.
 *
 *   Sync_Seg   1 TQ   fixed (§27.9.3)
 *   Prop_Seg   7 TQ   PRSEG<2:0>   = 110      875 ns
 *   Phase_Seg1 5 TQ   SEG1PH<2:0>  = 100
 *   Phase_Seg2 3 TQ   SEG2PH<2:0>  = 010
 *              -----
 *             16 TQ   sample point at 13/16 = 81.25 %, SJW = 2 TQ
 *
 * Against the rules in §27.11 and §27.9.7:
 *   Prop_Seg + Phase_Seg1 (12) >= Phase_Seg2 (3)   ok
 *   Phase_Seg2 (3) >= SJW (2)                      ok
 *   Phase_Seg2 >= IPT, which §27.9.7 fixes at 2 TQ for this family   ok
 *   bit time >= 8 TQ (§27.9.2, "the usable minimum is 8 TQ")   ok
 * and §27.9.6 asks for a sample point "as late as possible or approximately
 * 80 % of the bit time".
 *
 * WHY 7 TQ OF PROP_SEG AND NOT PICLIB'S 4. Three TQ move out of Phase_Seg1
 * into Prop_Seg. The bit rate does not change, the sample point does not move
 * -- it is (1 + 7 + 5)/16, the same 13/16 as (1 + 4 + 8)/16 -- and no other
 * register is touched. What it buys is margin on the two things Prop_Seg
 * actually pays for, and this board is unusual in both.
 *
 * 1. THE ROUND TRIP. §27.9.4: the propagation segment "compensate[s] for
 *    physical delay times within the network ... the signal propagation time
 *    on the bus line and the internal delay time of the nodes". Arbitration
 *    requires a bit to reach the far node and its answer to arrive back before
 *    the sample point, so the requirement is a round trip:
 *
 *      Prop_Seg >= 2 * (t_transmitter + t_cable + t_receiver)
 *
 *    DS20005167C §2.3, AC Characteristics: parameter 4, tTXD-BUSOFF = 125 ns
 *    max, and parameter 6, tBUSOFF-RXD = 110 ns max -- 235 ns through one
 *    node, which is exactly parameter 8's tTXD-RXD of 235 ns max, so the two
 *    ways of counting agree. Cable at 5 ns/m is a DECISION, not a datasheet
 *    number: it is the usual figure for twisted pair and nothing in this car
 *    has been measured. With L the one-way separation of the two nodes:
 *
 *      4 TQ = 500 ns:  500 >= 2 * (235 + 5*L)  ->  L <= 3.0 m
 *      7 TQ = 875 ns:  875 >= 2 * (235 + 5*L)  ->  L <= 40.5 m
 *
 *    Three metres is not a comfortable budget for a bus that runs from the
 *    engine bay to the dashboard, and the far node is not an MCP2562 -- it is
 *    whatever VW fitted, whose delays we do not have. Allowing 150 ns each way
 *    for it instead of 125/110 still fits in 875 ns (2 * (300 + 57) = 714 ns)
 *    and does not fit in 500.
 *
 * 2. THE STUB. This board hangs off the bus on an unterminated stub: about
 *    1.4 m of CANH/CANL from the instrument cluster to the air vent, and both
 *    120 R terminators are elsewhere in the car -- 60.1 R measured across CANH
 *    and CANL, which is what says they are both still there and that R5 on
 *    this board must stay unfitted.
 *
 *    1.4 m is an ESTIMATE AND STAYS ONE, deliberately. It was measured as
 *    1.3-1.4 m and the pessimistic end is carried everywhere; pinning it down
 *    would mean taking the dashboard apart again, which is not worth doing for
 *    a number the margin below swallows whole. Do not propose re-measuring it.
 *
 *    onsemi AND8376/D gives the usual limit for one unterminated stub as
 *
 *      L_STUB_MAX <= T_PROP_SEG / (50 * T_PROP(BUS))
 *
 *    which at 5 ns/m is 500/(50*5) = 2.0 m for the old split and
 *    875/(50*5) = 3.5 m for this one: the real stub goes from 1.4x margin to
 *    2.5x. That note is an application note about somebody else's
 *    transceivers, so by this repo's rules it is evidence and not a
 *    specification -- but it points the same way as the round trip above,
 *    which is the datasheet's.
 *
 * SJW = 2 TQ, and it costs nothing. §27.11 says "Typically, an SJW of 1 is
 * enough", which is advice for a bus whose oscillators you control. We are one
 * node on a car bus full of nodes we did not build and cannot measure, and SJW
 * is the bound on how much a resynchronisation may stretch Phase_Seg1 or
 * shorten Phase_Seg2 (§27.10.2) -- i.e. how much oscillator mismatch the node
 * can absorb. The standard bound is df <= SJW / (2 * 10 * NBT), which at
 * NBT = 16 TQ is 0.31 % at SJW = 1 and 0.63 % at SJW = 2. (That formula is
 * ISO 11898-1's, not DS39977C's; §27.12 only refers the reader there.) The
 * price is that Phase_Seg2 must be at least SJW, and 3 >= 2 with room.
 *
 * All of the above is arithmetic. What none of it is, is tested: CanSwitch.X
 * runs at 50 kbps, so BRP = 0 and this whole timing has been exercised on no
 * hardware at all. Watch the error counters the first time this listens to
 * the car.
 *
 * BRGCON1 = 01 000000: SJW<1:0> = 01 (2 TQ, Register 27-52), BRP<5:0> =
 *                      000000.
 * BRGCON2 = 1 0 100 110: SEG2PHTS = 1 (Phase_Seg2 freely programmable, which
 *                      it has to be to set 3 TQ), SAM = 0 (sampled once),
 *                      SEG1PH = 100 (5 TQ), PRSEG = 110 (7 TQ).
 * BRGCON3 = 1 0 000 010: WAKDIS = 1 (bus-activity wake-up disabled; this
 *                      device never sleeps), WAKFIL = 0, SEG2PH = 010 (3 TQ).
 *                      Unchanged -- Phase_Seg2 stays at 3 TQ.
 */
#define BRGCON1_500K        0x40u
#define BRGCON2_500K        0xA6u
#define BRGCON3_500K        0x82u

/* CIOCON, DS39977C Register 27-55.
 *
 * ENDRHI = 1: "CANTX pin will drive VDD when recessive", and the register's
 * own note 1 says "Always set this bit when using a differential bus to avoid
 * signal crosstalk in CANTX from other nearby pins."
 *
 * CLKSEL = 1: "Use the oscillator as the source of the CAN system clock"; 0
 * selects the PLL, and 0 is the reset value. PLLCFG is OFF in pic_config.h, so
 * the PLL is not running, and the datasheet nowhere says what the mux delivers
 * in that case. The bit rate is not a thing to leave to inference, so it is
 * set explicitly. (piclib leaves CLKSEL at its reset value; its bench test at
 * 50 kbps evidently survived that, which proves the mux is harmless there and
 * nothing more.)
 *
 * CIOCON = 0 0 1 0 000 1. */
#define CIOCON_CFG          0x21u

/* --- receive filters ------------------------------------------------------ */

/* The seven identifiers from config.h, in filter order. */
static const uint16_t k_rx_ids[] = {
    CAN_ID_SPEED,       /* 0x1A0 */
    CAN_ID_ENGINE,      /* 0x280 */
    CAN_ID_COOLANT,     /* 0x288 */
    CAN_ID_TANK,        /* 0x320 */
    CAN_ID_OIL,         /* 0x420 */
    CAN_ID_FUEL,        /* 0x480 */
    CAN_ID_ACCEL        /* 0x5A0 */
};

#define RX_FILTER_COUNT     (sizeof(k_rx_ids) / sizeof(k_rx_ids[0]))

/* Fourteen identifiers are broadcast periodically on this bus and we want
 * seven of them, so the filtering is worth doing in hardware rather than in
 * decode_frame(): at 500 kbps the half we throw away is half the interrupts,
 * half the FIFO pressure and half the bus reads.
 *
 * Mask: every one of the eleven identifier bits must match, and only standard
 * frames are accepted.
 *
 * DS39977C Register 27-41/27-42: RXMnSIDH carries SID<10:3> and RXMnSIDL
 * carries SID<2:0> in bits 7-5 plus, in Mode 1 and 2, an EXIDEN mask bit at
 * bit 3 -- "1 = Messages selected by the EXIDEN bit in RXFnSIDL will be
 * accepted; 0 = Both standard and extended identifier messages will be
 * accepted". Our filters all have EXIDEN = 0, so setting the mask bit is what
 * keeps extended frames out. */
#define RXM_SIDH_STRICT     0xFFu
#define RXM_SIDL_STRICT     0xE8u

/* --- helpers -------------------------------------------------------------- */

static bool can_set_mode(uint8_t mode)
{
    uint16_t guard;

    CANCON = (uint8_t)(mode << 5);

    for (guard = 0u; guard < MODE_TIMEOUT; guard++) {
        if ((uint8_t)((CANSTAT & 0xE0u) >> 5) == mode) {
            return true;
        }
    }

    return false;
}

/* Point the access-bank window at one of the CAN buffers, leaving MDSEL and
 * FIFOWM alone. */
static void can_window(uint8_t ewin)
{
    ECANCON = (uint8_t)((ECANCON & (uint8_t)~EWIN_MASK) | (ewin & EWIN_MASK));
}

/* DS39977C Register 27-37/27-38: SIDH is SID<10:3>, SIDL is SID<2:0> in bits
 * 7-5. EXIDEN (bit 3) stays clear, so the filter "will only accept standard ID
 * messages". The registers are not an array and the addresses are not
 * contiguous, hence the switch. */
static void can_set_filter(uint8_t index, uint16_t id)
{
    uint8_t sidh = (uint8_t)(id >> 3);
    uint8_t sidl = (uint8_t)((id & 0x07u) << 5);

    switch (index) {
    case 0u: RXF0SIDH = sidh; RXF0SIDL = sidl; break;
    case 1u: RXF1SIDH = sidh; RXF1SIDL = sidl; break;
    case 2u: RXF2SIDH = sidh; RXF2SIDL = sidl; break;
    case 3u: RXF3SIDH = sidh; RXF3SIDL = sidl; break;
    case 4u: RXF4SIDH = sidh; RXF4SIDL = sidl; break;
    case 5u: RXF5SIDH = sidh; RXF5SIDL = sidl; break;
    case 6u: RXF6SIDH = sidh; RXF6SIDL = sidl; break;
    default: break;
    }
}

/* --- initialisation -------------------------------------------------------- */

bool hal_can_init(hal_can_mode_t mode)
{
    uint8_t i;

    /* DS39977C §27.1 lists the initialisation sequence; the numbering below
     * is its own.
     *
     * 1. "Initial LAT and TRIS bits for RX and TX CAN." §27.1 again: "In
     *    normal mode, the CAN module automatically overrides the appropriate
     *    TRIS bit for CANTX. The user must ensure that the appropriate TRIS
     *    bit for CANRX is set." So TRISB3 is the one that matters; TRISB2 is
     *    set for the sake of being explicit. hal_sys_init() has already
     *    written both as part of the whole-register TRISB write.
     *
     *    LATB2 IS HIGH, NOT LOW, AND THAT IS THE WHOLE POINT. RB2 drives the
     *    MCP2562's TXD, and TXD is active low: DS20005167C §1.5 describes what
     *    the transceiver does about "Permanent dominant condition on TXD",
     *    which is to disable the CANH and CANL drivers after tPDT -- 1.25 ms
     *    typical, Table 1-4 parameter 11 -- "in order to prevent the
     *    corruption of data on the CAN bus". A driven-low TXD is a request to
     *    hold the bus dominant, and at 500 kbps 1.25 ms is over six hundred
     *    bit times of it. Recessive is idle; recessive is what an
     *    uninitialised pin must be.
     *
     *    It matters in three places. At power-up, because hal_sys_init() runs
     *    well before this function does. Here, because Configuration mode is
     *    entered next and the pin is ours throughout it. And permanently in
     *    Loopback, where §27.3.5 says "The TXCAN pin will revert to port I/O
     *    while the device is in this mode" -- so in loopback LATB2 is the only
     *    thing keeping a fitted transceiver off the bus. */
    LATBbits.LATB2 = 1;     /* recessive */
    TRISBbits.TRISB2 = 0;   /* CANTX */
    TRISBbits.TRISB3 = 1;   /* CANRX */

    /* 2. "Ensure that the ECAN module is in Configuration mode." §27.3.1: the
     *    configuration, mask, filter, mode-selection and bit timing registers
     *    are all locked outside it. */
    if (!can_set_mode(MODE_CONFIG)) {
        return false;
    }

    /* 3. "Select ECAN Operational mode" -- the functional mode, Mode 2 here.
     *    DS39977C Register 27-3 note 1: MDSEL "can only be changed in
     *    Configuration mode", which is where we are. */
    ECANCON = ECANCON_MODE2;

    /* All six programmable buffers stay receive buffers, which is what makes
     * the FIFO eight deep (§27.4.3, §27.5.3: "By default, all buffers are
     * configured as receive buffers"). Written out anyway -- the depth of the
     * FIFO is the whole argument for Mode 2 and should not rest on a default.
     * The three dedicated transmit buffers are untouched by this. */
    BSEL0 = 0x00u;

    /* 4. "Set up the Baud Rate registers." */
    BRGCON1 = BRGCON1_500K;
    BRGCON2 = BRGCON2_500K;
    BRGCON3 = BRGCON3_500K;
    CIOCON  = CIOCON_CFG;

    /* 5. "Set up the Filter and Mask registers." */
    RXM0SIDH = RXM_SIDH_STRICT;
    RXM0SIDL = RXM_SIDL_STRICT;

    for (i = 0u; i < (uint8_t)RX_FILTER_COUNT; i++) {
        can_set_filter(i, k_rx_ids[i]);
    }

    /* Every filter on Acceptance Mask 0. DS39977C Register 27-48/27-49: two
     * bits per filter, 00 = Acceptance Mask 0. Both registers reset to
     * something else (0x50 and 0x05), so this is not a no-op. */
    MSEL0 = 0x00u;
    MSEL1 = 0x00u;

    /* Every filter pointed at RXB0. DS39977C Register 27-47: a nibble per
     * filter, 0000 = RXB0. In Mode 2 the choice barely matters -- §27.4.3:
     * "There is no one-to-one relationship between the receive buffer and
     * acceptance filter registers. Any filter that is enabled and linked to
     * any FIFO receive buffer can generate acceptance and cause FIFO to be
     * updated" -- but RXFBCON1 and RXFBCON2 reset to 0x11, so they have to be
     * written to point somewhere inside the FIFO deliberately. */
    RXFBCON0 = 0x00u;
    RXFBCON1 = 0x00u;
    RXFBCON2 = 0x00u;
    RXFBCON3 = 0x00u;

    /* DS39977C Register 27-45: enable filters 0-6, disable 7-15. */
    RXFCON0 = 0x7Fu;
    RXFCON1 = 0x00u;

    /* Every buffer empty and accepting per the filters. RXM1 = 0 in each
     * control register means "Receive all valid messages as per acceptance
     * filters" (Register 27-13, 27-22); clearing RXFUL at the same time makes
     * sure a warm restart does not start out reading a stale frame. */
    RXB0CON = 0x00u;
    RXB1CON = 0x00u;
    B0CON = 0x00u;
    B1CON = 0x00u;
    B2CON = 0x00u;
    B3CON = 0x00u;
    B4CON = 0x00u;
    B5CON = 0x00u;

    /* Writing RXB0CON above went through the window, which ECANCON_MODE2 left
     * pointing at Receive Buffer 0 -- correct, but only by arrangement. Say so
     * again before leaving. */
    can_window(EWIN_FIFO_BASE);

    /* 6. "Set the ECAN module to normal mode." Or to one of the two silent
     * modes -- everything above is identical for all three, which is the
     * reason this is one function and not three: a listen-only build must
     * exercise the same filters, the same masks and the same bit timing as
     * the build that will follow it, or it has tested nothing that transfers.
     *
     * POLLING RATHER THAN INTERRUPTS. Nothing above enables a CAN interrupt
     * and nothing is going to. With an eight-deep FIFO and about four accepted
     * frames per 10 ms, the main loop -- which drains the FIFO every pass,
     * not merely every RX_POLL_MS -- has roughly a twenty-fold margin. The
     * alternative costs the one thing this design is short of: an interrupt
     * handler that would have to touch the same ECANCON window as the main
     * loop, with no lock available between them. */
    if (!can_set_mode((uint8_t)mode)) {
        return false;
    }

    g_mode = mode;
    return true;
}

bool hal_can_silent(void)
{
    return g_mode != HAL_CAN_MODE_NORMAL;
}

/* --- receive --------------------------------------------------------------- */

bool hal_can_receive(hal_can_frame_t *frame)
{
    const volatile uint8_t *src;
    uint8_t dlc;
    uint8_t i;

    /* DS39977C §27.15.1: "FIFO Pointer bits, FP<3:0> in the CANCON register,
     * point to the buffer that contains data not yet read. ... To determine
     * whether FIFO is empty or not, the user may use the FP<3:0> bits to
     * access the RXFUL bit in the current buffer. If RXFUL is cleared, the
     * FIFO is considered to be empty." */
    can_window((uint8_t)(EWIN_FIFO_BASE + (CANCON & 0x0Fu)));

    if (!RXB0CONbits.RXFUL) {
        return false;
    }

    /* Standard identifiers only. The mask forbids extended frames from ever
     * matching, so this cannot fire -- but an extended frame decoded as an
     * 11-bit identifier could collide with one of the seven we act on, and
     * that is not a failure worth leaving to a mask being right. */
    if (RXB0SIDL & 0x08u) {
        RXB0CONbits.RXFUL = 0;
        return false;
    }

    frame->id = (uint16_t)(((uint16_t)RXB0SIDH << 3) | (uint16_t)(RXB0SIDL >> 5));

    /* DS39977C Register 27-19: DLC<3:0> are bits 3-0. Clamping is belt and
     * braces -- decode_frame() honours dlc rather than assuming 8, and would
     * happily read past the end of an eight-byte array if handed a 9. */
    dlc = (uint8_t)(RXB0DLC & 0x0Fu);
    if (dlc > 8u) {
        dlc = 8u;
    }
    frame->dlc = dlc;

    src = &RXB0D0;
    for (i = 0u; i < dlc; i++) {
        frame->data[i] = src[i];
    }

    /* §27.15.1: "When receive data is no longer needed, the RXFUL bit in the
     * current buffer must be cleared, causing FP<3:0> to be updated by the
     * module." That is what advances the FIFO -- it is not a courtesy. */
    RXB0CONbits.RXFUL = 0;

    return true;
}

/* --- transmit -------------------------------------------------------------- */

static void tx_load(uint8_t ewin, uint16_t id, const uint8_t *data, uint8_t dlc)
{
    volatile uint8_t *dst;
    uint8_t i;

    /* The transmit buffers are not in the access bank, so this goes through
     * the window exactly as DS39977C Example 27-4 does it -- one copy of the
     * code for all three buffers rather than three. */
    can_window(ewin);

    /* Register 27-6/27-7: SIDH is SID<10:3>, SIDL is SID<2:0> in bits 7-5.
     * EXIDE stays clear: "Message will transmit standard ID". */
    RXB0SIDH = (uint8_t)(id >> 3);
    RXB0SIDL = (uint8_t)((id & 0x07u) << 5);

    /* Register 27-11: DLC<3:0> in bits 3-0, TXRTR clear -- a data frame. */
    RXB0DLC = (uint8_t)(dlc & 0x0Fu);

    dst = &RXB0D0;
    for (i = 0u; i < dlc; i++) {
        dst[i] = data[i];
    }

    /* Register 27-5: TXREQ is bit 3, TXPRI<1:0> the low two. All three of our
     * frames are equally unimportant to anyone else on the bus, so they go out
     * at priority 0 and the module arbitrates on identifier as usual. Same
     * value as Example 27-4's B'00001000'. */
    RXB0CON = 0x08u;
}

bool hal_can_send(uint16_t id, const uint8_t *data, uint8_t dlc)
{
    if (dlc > 8u) {
        dlc = 8u;
    }

    /* Listen Only transmits nothing (§27.3.4), so a queued frame would never
     * complete and TXREQ would never clear: the first three calls would fill
     * all three buffers and every call after that would return false anyway,
     * having left the module holding three stale frames for ever. Refusing up
     * front says the same thing without the wreckage.
     *
     * Loopback deliberately falls through to the real path. It is silent on
     * the wire too, but internally the frame is delivered to our own receive
     * FIFO, which is what makes it a test of anything. */
    if (g_mode == HAL_CAN_MODE_LISTEN_ONLY) {
        return false;
    }

    /* Three dedicated buffers and three frames per 100 ms, each about 230 us
     * on the wire: finding all three busy means the bus is saturated or we are
     * off it. TXREQ is readable without the window (TXBnCON has its own
     * address); only the loading needs it. */
    if (!TXB0CONbits.TXREQ) {
        tx_load(EWIN_TXB0, id, data, dlc);
        return true;
    }
    if (!TXB1CONbits.TXREQ) {
        tx_load(EWIN_TXB1, id, data, dlc);
        return true;
    }
    if (!TXB2CONbits.TXREQ) {
        tx_load(EWIN_TXB2, id, data, dlc);
        return true;
    }

    return false;
}

/* --- health ---------------------------------------------------------------- */

uint8_t hal_can_rx_errors(void)
{
    return RXERRCNT;
}

uint8_t hal_can_tx_errors(void)
{
    return TXERRCNT;
}

bool hal_can_overflow(void)
{
    /* DS39977C Register 27-4: in Mode 1 and 2 the overflow flag is COMSTAT
     * bit 6, RXBnOVFL, and §27.15.6.1: "An overflow condition occurs when the
     * MAB has assembled a valid received message ... and the receive buffer
     * associated with the filter is not available for loading of a new
     * message. ... This bit must be cleared by the MCU."
     *
     * The register is read-modify-written rather than assigned, and by number
     * rather than by bit name, because the mode-1/2 bit names differ from the
     * mode-0 ones and which of them a given XC8 device header defines is not
     * something to bet on. Bits 5-0 are read-only, so writing them back
     * changes nothing; bit 7 (FIFOEMPTY) is written back with the value just
     * read. */
    bool overflowed = (COMSTAT & 0x40u) != 0u;

    if (overflowed) {
        COMSTAT = (uint8_t)(COMSTAT & 0xBFu);
    }

    return overflowed;
}
