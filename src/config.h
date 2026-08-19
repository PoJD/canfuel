/* config.h -- every constant and switch of the converter in one place.
 *
 * Nothing here may depend on the PIC. The pure core (decode.c, compute.c,
 * txframes.c) includes this file and must stay compilable with gcc.
 *
 * Units are spelled out in every name because the whole core works in scaled
 * integers, not floats: an 8-bit PIC at 16 MHz has no floating point unit and
 * the accumulators have to be exact anyway.
 *
 *   _UL   microlitres          _MM   millimetres
 *   _MMH  0.001 km/h           _CNM  0.01 Nm
 *   _D    tenths (0.1 of the named unit)
 *   _C    hundredths (0.01 of the named unit)
 */
#ifndef CONFIG_H
#define CONFIG_H

/* --- CAN identifiers ---------------------------------------------------- */

/* Incoming, from the car. Documented in docs/can-decoding.md. */
#define CAN_ID_SPEED            0x1A0u  /* road speed + validity gate       */
#define CAN_ID_ENGINE           0x280u  /* rpm, throttle, load, torque      */
#define CAN_ID_COOLANT          0x288u  /* coolant temperature              */
#define CAN_ID_TANK             0x320u  /* fuel level, reserve lamp, doors  */
#define CAN_ID_OIL              0x420u  /* oil temperature                  */
#define CAN_ID_FUEL             0x480u  /* the fuel counter; no fixed period */

/* Outgoing, ours. Free on this bus -- see docs/frames.md. */
#define CAN_ID_TX_FUEL          0x600u  /* 100 ms */
#define CAN_ID_TX_ENGINE        0x601u  /* 100 ms */
#define CAN_ID_TX_TRIP          0x602u  /*   1 s  */
#define CAN_ID_TX_DIAG          0x603u  /*   1 s  */

/* --- the diagnostic frame, 0x603 ---------------------------------------- */

/* 0x603 exists so that "is this thing healthy" can be answered from the bus
 * instead of from a blink pattern somebody has to interpret. The ECAN error
 * counters are otherwise readable only by code running on the part: nothing
 * transmits them, IPECMD reads flash and EEPROM but not RAM, and a live read
 * would mean a debugger and the IDE this project does not use. So the LED was
 * the only instrument, and an LED asks a human to tell 2.5 Hz from 5 Hz
 * correctly, once, in a car, from an awkward angle.
 *
 * ⚠ **It is only transmitted while the DBG_EN jumper is fitted.** Nobody is
 * reading it in a closed dashboard, and a frame a second for nobody is bus
 * traffic and CPU we can decline to spend. JP1 already means "somebody is
 * looking at this device"; this is the second thing that means.
 *
 * ⚠ It cannot help in HAL_CAN_MODE_LISTEN_ONLY, and no frame could: that mode
 * transmits nothing at all (DS39977C §27.3.4). There the LED is still the only
 * channel there is. tools/bench_test.py reads this frame; docs/install.md
 * steps 7 and 9 are where it is used, and docs/frames.md is the layout.
 *
 * Nothing on the display reads it.
 *
 *   b0  ECAN receive error counter, RXERRCNT
 *   b1  ECAN transmit error counter, TXERRCNT
 *   b2  COMSTAT bits 5-0, the module's own error state (Register 27-4)
 *   b3  DIAG_FLAG_*, ours
 *   b4  bits 4-0 RESET_CAUSE_*, bits 7-5 DIAG_LAYOUT_VERSION
 *   b5  hal_can_send() refusals since power-up, saturating
 *   b6  uptime, seconds, high byte  } saturating at 0xFFFF, which is
 *   b7  uptime, seconds, low byte   } 18 hours
 *
 * The version shares a byte with the reset cause because all eight bytes are
 * spoken for and neither needs a whole one: five reset causes exist and three
 * bits of version is seven revisions of a frame that lives in one repository
 * and is pinned by test_txframes.c.
 */
#define DIAG_LAYOUT_VERSION     1u
#define DIAG_VERSION_SHIFT      5u
#define DIAG_RESET_CAUSE_MASK   0x1Fu

#define DIAG_FLAG_CAN_OK        0x01u   /* hal_can_init() reached its mode   */
#define DIAG_FLAG_SILENT        0x02u   /* a silent build -- loopback, since
                                         * listen only cannot transmit this  */
#define DIAG_FLAG_UNHEALTHY     0x04u   /* latched: an error or an overflow,
                                         * ever, since power-up             */
#define DIAG_FLAG_DATA_LIVE     0x08u   /* frames are arriving right now     */
#define DIAG_FLAG_PERSIST_OK    0x10u   /* persist_load() found a record     */
#define DIAG_FLAG_UNHEALTHY_NOW 0x20u   /* the same fault, but current       */

/* TWO FLAGS FOR ONE FAULT, AND THE LED FOLLOWS THE SECOND.
 *
 * The module's error counters walk back to zero on their own once the bus
 * behaves -- measured, from 128 to 0 -- so a fault that came and went leaves
 * no trace at all. That is what DIAG_FLAG_UNHEALTHY is for, and why it never
 * clears: it is the only thing that can say "something happened while nobody
 * was looking".
 *
 * The cost of driving LED_CAN from it is that one transient blinks the LED
 * until the next reset, and after that the light says nothing about now.
 * DIAG_FLAG_UNHEALTHY_NOW is the live half: set while an error counter is
 * non-zero or an overflow has just been seen, and held for a moment
 * afterwards, because an overflow is an instant and a 100 ms blink is not
 * something anybody can see. The LED follows this one, so it goes out when the
 * bus recovers; the frame keeps both, so the history is not lost.
 *
 * The hold counts down once per TX_FAST_MS, in the slot that reads the
 * counters, so fifteen of them is 1.5 s: long enough that a single overflow is
 * unmistakable, short enough that the light stays honest about the present. */
#define DIAG_UNHEALTHY_HOLD     15u

/* Why the part last started, out of RCON and STKPTR -- see hal_sys.h. Zero is
 * a legitimate answer: an MCLR reset is none of these, and that is what a
 * programmer leaves behind. */
#define RESET_CAUSE_POWER_ON    0x01u
#define RESET_CAUSE_BROWN_OUT   0x02u   /* the car's supply sagged past BORV */
#define RESET_CAUSE_WATCHDOG    0x04u   /* a hang; the one that means a bug  */
#define RESET_CAUSE_RESET_INSTR 0x08u
#define RESET_CAUSE_STACK       0x10u   /* STKFUL/STKUNF, with STVREN on     */

/* --- which ECAN mode the firmware starts in ----------------------------- */

/* One of the HAL_CAN_MODE_* names from hal_can.h, which is where the three
 * modes and the reasons for them are documented. Normal is the converter;
 * the other two are diagnostic builds that put nothing on the wire.
 *
 * It is deliberately a compile-time choice and not a jumper. The obvious
 * jumper is JP1/DBG_EN, and overloading it would be a trap: DBG_EN means "the
 * LEDs may light", which is exactly as useful while transmitting as while
 * listening, so the two have no reason to move together.
 *
 * Overridable from the build, so that a diagnostic hex needs no edit here and
 * leaves no chance of one being committed by accident:
 *
 *     make -C mplab CAN_MODE=LISTEN_ONLY
 *     make -C mplab CAN_MODE=LOOPBACK
 */
#ifndef CAN_START_MODE
#define CAN_START_MODE          HAL_CAN_MODE_NORMAL
#endif

/* --- the supply reading, and the one calibration it can have ------------- */

/* VddConv IS CALIBRATED PER UNIT, AND HAS TO BE.
 *
 * The firmware measures the internal 1.024 V band gap against VDD and inverts
 * it, so the whole reading rests on that 1.024 V -- and DS39977C gives it **no
 * tolerance anywhere**. The figure appears only in the channel list of
 * Register 23-1; Section 31.0 has no min, typ or max for it. On the one board
 * measured, the nominal arithmetic was out by 4.1 %, which is 0.20 V on a 5 V
 * rail and quite enough to send somebody chasing a supply fault.
 *
 * THE VALUE BELOW IS BOARD 1's. If you are building from install.md it is
 * somebody else's part and somebody else's band gap. Recalibrate, or accept a
 * few per cent -- nothing downstream of VddConv is a decision, so an
 * uncalibrated reading is untidy rather than dangerous.
 *
 * HOW TO CALIBRATE, from any starting point including this one:
 *
 *   1. Put a meter on U1 pin 20 against pin 19 with the converter running and
 *      transmitting, and read VddConv out of 0x601 at the same moment. The
 *      rail sags a little under bus traffic, so a pair taken seconds apart is
 *      not a pair.
 *   2. VDD_NUMERATOR_C = VDD_NUMERATOR_C x meter / shown, both in 0.01 V.
 *   3. Rebuild, reflash, and check the two agree.
 *
 * It is written as the numerator rather than as the pair of readings on
 * purpose: the pair only means anything alongside the numerator that was in
 * force when it was taken, and a constant that cannot be re-derived from its
 * own comment is a trap. Starting from scratch means starting at
 * VDD_NOMINAL_C.
 *
 * TAKE THE SHOWN VALUE AS A MEAN, NOT AS ONE READING. 299 consecutive samples
 * off board 1 spanned 4.86 to 4.91 V with a mean of 4.876 -- so the A/D's own
 * scatter is about +/-0.025 V, which is five times the 0.005 V an LSB is worth
 * at this code. Calibrating against a single frame chases that scatter: the
 * first two passes here landed 0.03 V high and then 0.03 V low while the rail
 * and the meter both sat still. `canlog.py --dump --id 0x601` over half a
 * minute is the reading to use.
 *
 * Board 1: mean 4.876 shown against 4.89-4.90 on the meter, both with the bus
 * running. The reading is not more precise than the scatter, and there is no
 * point pretending otherwise -- what this buys is the 4.1 % systematic error
 * gone, not a third decimal place. */
#define VDD_NUMERATOR_C         436344UL

/* VddConv IS FILTERED, because the A/D's scatter is bigger than its LSB.
 *
 * One conversion is good to about +/-0.025 V on the board measured -- five
 * times what an LSB is worth at this code -- so an unfiltered reading walks
 * the last digit of the display around at ten changes a second for no reason.
 * Nothing in the car changes the supply that fast except cranking, and that is
 * the brown-out detector's job rather than this field's.
 *
 * First order, in the same shape as the tank filter in compute.c: the value is
 * carried at 1/32 of a hundredth of a volt -- which keeps it inside a uint16,
 * and the 32-bit version of the same filter cost 518 bytes -- and each new
 * sample moves it by 1/16 of the difference. At the ten samples a second slot 0 gives, that is a
 * time constant of about 1.6 s and it divides the scatter by about four. A
 * shift keeps it a shift; do not make this a divisor. */
#define VDD_FILTER_SHIFT        4

/* The uncalibrated numerator, and where to start from:
 *
 *   VDD = 1.024 x 4096 / code, and in 0.01 V that is 100 x 4194.304 / code
 *
 * 4096 and not 1023: this A/D is twelve bits (DS39977C Table 31-25, parameter
 * A01) and the ten-bit formula from a different PIC would report four times
 * the real supply. */
#define VDD_NOMINAL_C           419430UL

/* --- timing ------------------------------------------------------------- */

/* ONE FRAME PER SLOT, AND IT IS A CORRECTNESS RULE RATHER THAN TIDINESS.
 *
 * The four transmitted frames used to be sent in two bursts -- 0x600 and 0x601
 * back to back every 100 ms, 0x602 and 0x603 behind them once a second. At
 * 500 kbps a frame is about 230 us on the wire, so that is three or four
 * frames inside a millisecond, from one node, with no gap between them.
 *
 * MEASURED ON THE BENCH: A RECEIVER WITH TWO BUFFERS LOSES THE THIRD ONE.
 * Both USBtin adapters (MCP2515) dropped whichever of our frames came third on
 * the wire, silently, without setting their own overrun flag, and on an
 * otherwise empty bus -- so it is not throughput. Moving a frame out of the
 * burst restored it to exactly its nominal rate; moving a different frame into
 * the burst broke that one instead. Two directions, same hardware.
 *
 * WHICH FRAME IS THIRD IS NOT WHICH SEND IS THIRD. DS39977C 27.6.3: buffers of
 * equal priority go out highest buffer number first, and all of ours are
 * priority 0, so the wire order depends on which of TXB0..TXB2 happened to be
 * free. That is why the symptom moved between 0x601, 0x602 and 0x603 as the
 * code around it changed, and why it cannot be reasoned about from the order
 * of the hal_can_send() calls.
 *
 * The converter was never at fault: the module reported every one of those
 * frames as successfully transmitted, which in CAN requires an acknowledgement
 * from another node. So this is insurance, not a repair. It is bought because
 * the MFD15 is a small device too, because nothing can be instrumented once
 * the dashboard is closed, and because every future bench measurement would
 * otherwise carry a hole exactly where one of our frames lands third.
 *
 * So the scheduler emits AT MOST ONE FRAME PER SLOT and the slot is 25 ms:
 *
 *   slot & 3 == 0   0x600, ten times a second
 *   slot & 3 == 1   0x601, ten times a second, 25 ms behind it
 *   slot == 2       0x602, once a second
 *   slot == 3       0x603, once a second (with JP1 fitted)
 *   slot == 22      the EEPROM slot, 550 ms, in a slot that sends nothing
 *
 * Nothing on the wire changes rate: both fast frames are still 10 Hz and both
 * slow ones still 1 Hz, so S-AQY.TRI is untouched. */
#define TX_SLOT_MS              25      /* one frame per slot, never two      */
#define TX_SLOTS_PER_SEC        40      /* 40 x 25 ms = one second            */
#define TX_SLOT_TRIP            2       /* 0x602 at 50 ms                     */
#define TX_SLOT_DIAG            3       /* 0x603 at 75 ms                     */
#define TX_SLOT_PERSIST         22      /* 550 ms, and sends nothing          */

#define TX_FAST_MS              100     /* 0x600 and 0x601, four slots apart  */
#define TX_SLOW_MS              1000    /* 0x602, 0x603 and the EEPROM slot   */
#define RX_POLL_MS              10      /* scheduler slot that drains the CAN */

/* The step distance is integrated on. NOT every pass of the scheduler, and the
 * difference is worth several per cent of every distance this device reports.
 *
 * A pass of the main loop takes about 113 us, so integrating on every one of
 * them hands compute_tick() a delta of a single millisecond -- and
 * v [0.001 km/h] * 1 ms / 3600 is then truncated to a whole millimetre, a
 * thousand times a second. At 100 km/h that throws away 0.78 mm of every
 * 27.78 (-2.8 %), at 50 km/h 0.89 of every 13.89 (-6.4 %), and BELOW 3.6 km/h
 * the quotient is zero, so the car covers no distance at all. It goes straight
 * into total_mm, and from there into FuelAvg, Range and the trip.
 *
 * Ten milliseconds makes each truncation ten times smaller and the remainder
 * carried in compute_t (dist_rem) removes what is left, so the integration is
 * exact and cannot drift. The division count falls from ~1000/s to 100/s with
 * it, which is the largest single saving in the firmware -- but the reason for
 * the change is the arithmetic, not the cycles.
 *
 * Why 10 and not 100: 0x1A0 arrives at 130 Hz, so a 10 ms step still samples
 * the speed faster than the car sends it, while a 100 ms one would integrate
 * an acceleration from its end point and overstate it. Why not 1: that is what
 * the paragraph above is about.
 *
 * NOTHING IN THE FIXTURES EVER SAW THIS. test/replay_core.h drives
 * compute_tick() from the 0x480 frames, which are ~38 ms apart, so the tests
 * integrate with a delta at which the truncation is 0.8 % and invisible under
 * the tolerance replay.py compares on. It is a hardware-only fault, found by
 * reading rather than by running. */
#define DIST_TICK_MS            10u

/* Below this the car is standing still and the distance integrator must see
 * nothing at all.
 *
 * A STANDING CAR DOES NOT SEND ZERO. 0x1A0 reads raw 1 -- 0.005 km/h, or
 * 1.39 mm/s -- in every log while stationary, and the next value that ever
 * appears is above raw 40 (0.2 km/h); nothing in between exists in any
 * fixture. It is the same measurement STANDSTILL_MMH rests on and the
 * same number, kept as a separate name because the two guard different things
 * and have no reason to move together.
 *
 * THIS IS DECIDED, NOT HIDDEN. With a one-millisecond step the
 * quotient of anything under 3.6 km/h was zero, so the standing value
 * integrated to nothing by accident. Making the integration exact turned that
 * accident into 83 mm over a minute of idling -- which 02_idle_60s and
 * 01_ign_only caught the moment the remainder was carried. */
#define DIST_MIN_MMH            100u        /* 0.1 km/h */

/* The bus is declared dead after this long without a fuel frame; every
 * transmitted value then goes to zero rather than freezing at its last
 * reading, which would look plausible and be wrong. */
#define DATA_TIMEOUT_MS         500u

/* Sliding window the instantaneous flow is averaged over, as four quarter
 * second buckets rather than one slot per frame.
 *
 * 0x480 has NO fixed period -- measured with adapter timestamps it is 26.4
 * frames/s at idle and 18.0 at 2586 rpm, on a 10 ms grid (can-decoding.md
 * question 1) -- so nothing here may assume a rate. The window is a whole
 * number of buckets: each frame is added into the open bucket, and the bucket
 * closes as soon as it holds FLOW_BUCKET_MS, so the four together span 1.00 to
 * 1.03 s in practice.
 *
 * A 32-SLOT RING of (microlitres, milliseconds) was rejected, with the oldest
 * samples dropped one at a time until the window fitted a second. That is 128
 * bytes of RAM, a drop loop, and -- because the answer was recomputed on every
 * frame -- **a 32-bit division by a variable twenty-six times a second**, at
 * 1,026 cycles each, for a number transmitted ten times a second. The buckets
 * divide four times a second instead, which is still more often than the
 * display can show a change.
 *
 * What it costs: the flow steps four times a second rather than continuously,
 * and the window is 0.75-1.0 s of history at the moment it is read rather than
 * exactly 1.0. Neither is visible on a gauge reading 0.1 l/h.
 *
 * FLOW_WINDOW_MS is now the gap that invalidates the window rather than its
 * length: a frame further than this from the last one describes a different
 * situation entirely, and the bus is declared dead at half of it anyway
 * (DATA_TIMEOUT_MS). It also bounds what a single bucket can hold, which is
 * what keeps the uint16 fields in flow_sample_t from overflowing. */
#define FLOW_WINDOW_MS          1000u
#define FLOW_BUCKET_MS          250u
#define FLOW_BUCKETS            4

/* --- fuel counter ------------------------------------------------------- */

/* The counter in 0x480 b2-b3 is 15 bits; bit 15 is a wrap flag, not data, and
 * the mask simply drops it. Trap 3 in docs/can-decoding.md records what that
 * bit does -- it is zero from ignition on until the first wrap and then
 * permanently one -- but nothing here reads it. */
#define COUNTER_MODULO          32768u
#define COUNTER_MASK            0x7FFFu

/* --- speed validity gate ------------------------------------------------ */

/* Byte 1 of 0x1A0 is a bit field. It is NOT an equality test -- getting this
 * wrong throws away two thirds of the samples. docs/can-decoding.md, trap 1. */
#define SPEED_GATE_REQUIRED     0x40u   /* this bit must be set              */
#define SPEED_GATE_FORBIDDEN    0x03u   /* these mark the post-ignition ramp */

/* --- FuelNow, the dual-unit channel ------------------------------------- */

/* Below this speed FuelNow carries l/h, at or above it l/100 km. A single
 * threshold, no hysteresis: the jump is the visual cue that it switched.
 * Why 4 and not 3 km/h is argued in docs/frames.md. */
#define FUELNOW_LH_BELOW_MMH    4000u   /* 4.000 km/h */

/* 99.9 on the display. The TRI gauge tops out there and behaves
 * unpredictably above it, so everything is clamped before transmission. */
#define FUELNOW_CLAMP_D         999u

/* --- FuelAvg ------------------------------------------------------------ */

/* Below this distance the average divides by nearly zero. On 06_trip_reset
 * that produced 21,395 l/100 km before the car had moved at all. */
#define AVG_MIN_MM              100000ul    /* 100 m */

/* THE OTHER END OF THE SAME PROBLEM: the trip is capped, and this is a safety
 * net rather than a feature.
 *
 * Nothing clears the accumulators except a detected refuelling. If the tank
 * sender fails, or reads plausibly but never rises -- or the rule simply never
 * fires -- they grow without bound, and total_mm is millimetres in a uint32_t,
 * so at 4,295 km it WRAPS. Silently: the distance restarts near zero while the
 * fuel total does not, and FuelAvg becomes whatever that ratio is. A tank is
 * about 600 km, so reaching this needs a fault -- and a fault is exactly what
 * a safety net is for.
 *
 * 2,000 km IS A DECISION, and the maintainer's: it is more than three
 * tankfuls, an average taken over such a distance means nothing to him, and it
 * sits at 47 % of the point where the arithmetic breaks. Nothing of value is
 * lost by starting again there.
 *
 * The litre cap is the same rule for the other accumulator. Distance alone
 * cannot bound it, because idling burns fuel and covers no ground: 400 l is
 * what 2,000 km costs at 20 l/100 km, and reaching it any other way takes
 * months of continuous idling.
 *
 * WHY IT RESETS RATHER THAN SATURATES. Saturating would freeze a number that
 * is already meaningless -- an average across three tankfuls and a broken
 * sender -- and freeze it for ever, because only a refuelling would ever
 * release it. Resetting says what actually happened: we lost track, here is a
 * fresh average that means something. It goes through compute_reset_trip(),
 * the same path a refuelling takes, so Range falls back to its conservative
 * default for the first 5 km exactly as it does after filling up. It does NOT
 * count as a refuelling -- `refuels` keeps meaning "the tank was seen to
 * rise", and a diagnostic that lies about why is worse than no diagnostic. */
#define TRIP_MAX_MM             2000000000ul    /* 2 000 km */
#define TRIP_MAX_UL             400000000ul     /*   400 l  */

/* --- Range -------------------------------------------------------------- */

/* The basis Range divides by: a rolling consumption figure updated once per
 * kilometre, so the estimate falls gradually after a hard pull rather than
 * jumping.
 *
 * A FLAT AVERAGE OVER THE LAST 30 KILOMETRES was rejected, held as 30
 * microlitre totals -- 120 bytes of RAM that were summed on every gather, ten
 * times a second, to produce a number that can only change once a kilometre.
 * It is a first-order filter now, one shift per completed kilometre, which is
 * the same idea with none of the storage: mean age 16 km against the flat
 * window's 15, so the estimate is very nearly as steady and reaches a new
 * consumption level at much the same rate.
 *
 * The filter carries four extra bits (RANGE_BASIS_Q4) and that is not
 * decoration. In whole tenths of l/100 km a shift of four cannot move a value
 * below 1.6 l/100 km of difference at all, so the filter would stall a long
 * way from the truth; with the extra bits it stalls within 0.1 l/100 km, which
 * is one digit of the average shown beside it. */
#define RANGE_SEGMENT_MM        1000000ul   /* 1 km */
#define RANGE_BASIS_SHIFT       4u          /* tau = 16 km                  */
#define RANGE_BASIS_Q4          4u          /* the basis is in 1/16 tenths  */

/* Until this much has been driven the rolling window is too short to trust,
 * so a conservative fixed figure is used instead. */
#define RANGE_MIN_MM            5000000ul   /* 5 km */
#define RANGE_DEFAULT_L100_D    90u         /* 9.0 l/100 km */

/* --- tank level and the refuelling reset -------------------------------- */

/* The instantaneous level is unusable: standing it varies by 2-3 L, driving
 * by 9-10 L because the float sloshes. The value taken at rest is rock solid.
 * docs/refuel-reset.md has the measurements. */
#define TANK_SAMPLE_MS          1000u       /* one sample per second        */
#define TANK_STATIONARY_MMH     1000u       /* "at rest" is below 1 km/h    */

/* The settled level -- the baseline a refuelling is judged against -- is a
 * first-order filter over the at-rest samples, one shift per sample, so this
 * is a time constant of 16 seconds at TANK_SAMPLE_MS.
 *
 * A MEDIAN of a 25-slot ring read out of a 128-bucket histogram was
 * rejected. The reasoning is in docs/optimisation.md: the median was our choice rather than a requirement,
 * it cost 2,453 cycles and 153 bytes of RAM, and what it was actually being
 * asked for -- "is the level suddenly and persistently higher than it was" --
 * is answered by the counter below without sorting or counting anything.
 *
 * A shift and not a divisor: on this part a division by a non-power of two is
 * a reciprocal multiply, and the whole filter is two bytes of state and one
 * rotate this way. 16 s is long enough to sit still through the 2-3 L the
 * sender wanders at rest and short enough to have settled by the time anybody
 * has finished refuelling. */
#define TANK_REST_SHIFT         4u          /* 1/16 per sample, tau = 16 s  */

/* A rise of more than this above the settled level means somebody refuelled,
 * and the trip accumulators are cleared -- but only after this many
 * CONSECUTIVE at-rest samples say so.
 *
 * WHY A COUNTER RATHER THAN A MEDIAN. The asymmetry in docs/refuel-reset.md
 * governs: a missed refuelling costs one late reset, a false one silently
 * destroys an average the driver has watched for 600 km. A median rejected a
 * single outlier by construction; five consecutive seconds rejects it by
 * evidence, and rejects a sustained one that a median of 25 would have let
 * through once it reached the thirteenth sample. Five is also what the median
 * needed before it was trusted at all (TANK_MEDIAN_MIN, gone with it), so the
 * sequence at a filling station -- ignition off, ring empty on the next start,
 * driver pulls away within seconds -- is no worse off than before.
 *
 * The baseline is deliberately FROZEN while the counter is running, or the
 * filter above would chase the new level and disqualify a rise it was in the
 * middle of confirming. compute.c does that in one branch. */
#define REFUEL_RISE_L           3u
#define REFUEL_CONFIRM_S        5u

/* First-order damping of the transmitted tank level, in samples at
 * TANK_SAMPLE_MS -- so this is the time constant in seconds. It feeds both the
 * displayed level and the range.
 *
 * It was 60. Measured against the fixtures, the filter turns the float's slosh
 * into this much residual ripple:
 *
 *   07_accel (driving, raw spread 10 L)   60 s -> 0.44 L    120 s -> 0.18 L
 *   06_trip_reset (near empty, spread 8)  60 s -> 3.45 L    120 s -> 2.67 L
 *
 * In range that is 5 km of swing against 2 on the first and 38 against 29 on
 * the second. A DECISION, not a measurement: 120 s halves the ripple, and what
 * it costs -- 90 % of any step in about 4.6 minutes instead of 2.3 -- costs
 * nothing here, because the only fast change a tank ever makes is refuelling
 * and compute.c now snaps straight to the median when it detects one. Fuel
 * being burnt moves the level over hours.
 *
 * 06_trip_reset is the honest caveat: it was recorded with the reserve lamp on
 * and the sender at the bottom of its travel, where it is at its worst, and no
 * amount of damping makes that reading good.
 *
 * 128 AND NOT 120, and the eight seconds are not the point.
 * A divisor that is not a power of two is a reciprocal multiply on this part --
 * mulhi_u32 plus a rotate, about 360 cycles -- where a power of two is the
 * rotate alone, about 70. The time constant was a decision inside a range
 * where 60 and 120 were both defensible, so moving it 7 % to buy that is free;
 * what it also buys is one fewer magic number in divconst.h to derive and
 * prove. The dead zone the integer step leaves grows from 0.120 l to 0.128,
 * which is still one digit of the display. */
#define TANK_DAMP_SAMPLES       128u
#define TANK_DAMP_SHIFT         7u          /* 2**7 = TANK_DAMP_SAMPLES */

/* --- torque and power --------------------------------------------------- */

/* Indicated torque is 0x280 b7, one byte, full scale 255.
 *
 * THE SCALE IS A DECISION, NOT A MEASUREMENT. The ME7 does not send Nm: b7 is
 * a percentage of a reference torque that lives in the ECU's calibration, at
 * ~0.39 % per bit (mfd15/docs/sensors.md §8). Turning that into Nm needs to
 * know what 100 % refers to, and nobody here has that number.
 *
 * 0.67 Nm/bit is WRONG here, and comes from "the maximum is 172 Nm, so
 * 172/256 = 0.67". That premise contradicts the rest of the model, and
 * 05_rev3000 is what proves it: at 2940 rpm in neutral the crank is putting
 * out nothing at all, and b7 still reads 37. A signal scaled to crank torque
 * would read zero there. So b7 is indicated torque -- what the combustion
 * makes, before friction -- and its full scale is the maximum INDICATED
 * torque, which is the rated crank figure plus the drag at that speed.
 * Scaling to 172 Nm and then subtracting drag on top counts the friction
 * twice, and the firmware could never display what the engine is sold as.
 *
 * The AQY is rated 85 kW at 5200 rpm and 170 Nm at 2400 rpm (115 PS is the
 * horsepower figure, not a torque one). Requiring b7 = 255 to reproduce each
 * rating in turn brackets the scale -- and the bracket MOVES WITH THE DRAG
 * LINE, because what b7 = 255 has to cover is the rated crank figure plus the
 * drag at that speed. On the cold-oil drag line the bracket was 0.745 to
 * 0.773 and 0.75 was chosen inside it. On the warm line below it is
 *
 *   85 kW at 5200 rpm   -> 0.736 Nm/bit
 *   170 Nm at 2400 rpm  -> 0.738 Nm/bit
 *
 * which is a bracket 0.3 % wide rather than 3.7 %, so the two factory ratings
 * now agree with each other about the scale instead of arguing. 0.74 sits
 * inside it and reproduces both to better than 0.5 %: 85.4 kW at 5200 rpm and
 * 170.4 Nm at 2400 rpm, against 85 and 170.
 *
 * Do not read that agreement as proof. The constraint is dominated by the
 * SLOPE of the drag line; the intercept moves the two endpoints together, so
 * a wrong intercept can still look consistent here. It is a check that passed,
 * not a measurement.
 *
 * What would settle it: nothing available. The VCDS session was done on
 * This ECU has no torque measuring block --
 * groups 001, 002, 003 and 020 offer engine load in per cent and nothing in
 * Nm. The only remaining route is a full-throttle pull, which is deliberately
 * not planned. The question is therefore parked, not open: see
 * docs/can-decoding.md, chapter "Never resolved but not required", question 8.
 * test_compute.c pins the ceiling so that a future change cannot quietly put
 * the factory figures out of reach again. */
#define TORQUE_CNM_PER_BIT      74u         /* 0.74 Nm -- see above */

/* Drag torque -- friction, pumping, alternator -- rises with engine speed and
 * is modelled linearly:
 *
 *   drag_cnm = BASE + rpm * SLOPE / 10000
 *
 * FITTED on the four warm free-revving holds, rather than a line
 * through two COLD-OIL fixture points. Stationary, in neutral, oil 72.8-76.6 C
 * off 0x420 b3, ~2,375 frames of 0x280 averaged per hold:
 *
 *   13_rev1500_z1   1536 rpm, b7 = 18.81, oil 72.8 C, throttle 48
 *   14_rev1850_z1   1850 rpm, b7 = 20.66, oil 74.2 C, throttle 51
 *   15_rev2372_z1   2372 rpm, b7 = 26.32, oil 75.3 C, throttle 56
 *   16_rev2926_z1   2926 rpm, b7 = 27.23, oil 76.6 C, throttle 61
 *
 * In neutral the crank drives nothing, so net torque is zero at every one of
 * them and b7 IS the drag there. Least squares gives, in bytes,
 *
 *   drag_b7 = 9.11 + 0.006514 * rpm     residuals -0.9 to +1.8 counts
 *
 * and BASE/SLOPE below are that line times TORQUE_CNM_PER_BIT. The calibration
 * is in BYTES, not Nm -- change the scale and this must be refitted with it.
 *
 * What it replaces and why. The old line was fitted on 02_idle_60s (60.8 C)
 * and 05_rev3000 (39.0 C), and cold oil overstates drag most exactly where the
 * fit is most sensitive to it. Since this is SUBTRACTED from indicated torque,
 * an overstated drag understates torque and power on the display: the old line
 * showed zero for 51 % of 17_drive_property_z1, where the new one shows a
 * number for 78 % of it. Peak torque over that drive barely moves (105.8 ->
 * 107.0 Nm) because at high load the drag is a small term; the whole
 * difference is at part throttle, which is where a driver spends the time.
 *
 * THE IDLE POINT IS DELIBERATELY EXCLUDED, AND THE DRIVING GATE COVERS IT.
 * 11_idle_noac_z1 is 798 rpm at b7 = 24.96 on the same warm oil, which is ABOVE
 * the line the other four make -- b7 falls 24.96 -> 18.81 between idle and
 * 1536 rpm and only then starts rising. Idle is a different state: the
 * throttle is at its rest position 38 against 48-61 for the holds, so the
 * pumping loss against a nearly closed throttle is large, and the ECU is
 * regulating speed rather than letting the engine free-rev. A straight line in
 * rpm cannot pass through both, so idle is ASSERTED rather than fitted -- see
 * STANDSTILL_MMH and THROTTLE_REST below, which return zero outright whenever
 * the car is not moving or the pedal is not pressed, which is every state the
 * engine idles in. Do not "fix" the residual by raising BASE: that puts the
 * line back above all four measured points and restores the understatement the
 * refit removed, and the gate has already dealt with the only places it
 * showed.
 *
 * STILL NOT HOT. 72-77 C is warm, not the 95-110 C of real driving, so this
 * line very likely still overstates drag a little -- which is the conservative
 * direction. Question 7 in docs/can-decoding.md stays open for exactly that,
 * and is the only open question left.
 *
 * THE SLOPE IS SCALED BY 2**16, NOT BY 10,000. It is our own
 * fixed-point choice and nothing outside this file reads it, so a power of two
 * makes the division a free byte shift instead of a reciprocal multiply and a
 * 13-bit rotate -- and takes another magic number out of divconst.h. The line
 * did not move: 31589/65536 = 0.4820023 against 0.4820, which is 5 parts per
 * million of a slope whose measurement uncertainty is percent. To refit, work
 * in bytes as above and multiply the b7 slope by TORQUE_CNM_PER_BIT * 65536. */
#define DRAG_TORQUE_BASE_CNM    674l        /* 6.74 Nm at 0 rpm  (9.11 b7)  */
#define DRAG_TORQUE_SLOPE_Q16   31589l      /* 0.4820 cNm per rpm, x 2**16  */

/* THE DRIVING GATE. Torque and power are displayed only while the car is
 * MOVING and the driver is ASKING FOR TORQUE. Standing still shows zero
 * whatever the pedal is doing, and a released pedal shows zero whatever the
 * speed is. This is A FIXED REQUIREMENT, NOT A CALIBRATION: it holds on cold
 * oil and on hot, at any idle speed the ECU chooses, and it is not to be
 * relaxed or made conditional by any future refit of the drag line.
 * test_compute.c asserts both halves directly and test_txframes.c asserts
 * them on the assembled frame.
 *
 * IT USED TO BE AN AND AND IT IS NOW AN OR, and that is the whole change.
 * Gating on "standing AND released" left two states on the display that the
 * car is not in:
 *
 *   REVVING IN NEUTRAL AT A STANDSTILL showed a number. The crank drives
 *   nothing there -- that is exactly what makes the four free-revving holds a
 *   calibration rather than data -- so the honest answer is zero. 1,528
 *   samples of 17_drive_property_z1 are this state.
 *
 *   ROLLING TO A STOP OFF THE THROTTLE showed a number for the last few
 *   seconds of every stop, after showing zero for the part before it. High in
 *   the deceleration the ECU cuts fuel, b7 falls below the drag line and the
 *   answer is zero; once engine speed drops back onto the idle governor b7
 *   climbs 7 -> 27 while the pedal never moves, and 27 is well above what the
 *   drag line claims at 800 rpm. Off one real stop in 17_drive_property_z1,
 *   with the throttle at 38 throughout:
 *
 *       19.6 km/h  1358 rpm  b7 7    ->  0.0 Nm
 *       13.5 km/h   898 rpm  b7 17   ->  1.5 Nm
 *        8.0 km/h   792 rpm  b7 25   ->  8.0 Nm
 *        3.8 km/h   783 rpm  b7 27   ->  9.5 Nm
 *        standing   776 rpm  b7 27   ->  0.0 Nm   (the old gate, at last)
 *
 *   The apparent threshold is engine speed returning to idle, not road speed;
 *   in first gear the two coincide near 4-8 km/h, which makes it look like a
 *   speed threshold and is a coincidence of gearing.
 *
 * BOTH ARE THE SAME FAULT: the drag line is systematically LOW at idle. b7 is
 * 25 there against the 14 the line predicts at 800 rpm, and no straight line
 * in rpm can pass through both idle and the free-revving holds, because at
 * idle the throttle is nearly shut and the pumping loss is large while the ECU
 * regulates speed. So idle is ASSERTED rather than fitted -- and the assertion
 * has to cover every state the engine idles in, not only the parked one.
 * Fitting idle instead is what the old cold-oil line effectively did, and it
 * understated torque everywhere the car is actually driven.
 *
 * WHAT IT COSTS, because it is not free. Over 17_drive_property_z1 the share
 * of samples displaying zero goes 28.4 % -> 58.0 % (the peak does not move:
 * 107.0 Nm). That log is six minutes of first-gear pottering with a great deal
 * of coasting, so it is the worst case rather than a typical drive. And
 * PULLING AWAY NOW READS ZERO UNTIL THE CAR MOVES -- a median of 0.7 s after
 * the pedal leaves rest across the 14 pull-aways in that log, 1.75 s at worst.
 * Real torque against a slipping clutch is not shown for that time. Accepted
 * deliberately: a stationary car showing a number is the thing being fixed.
 *
 * The construction is not ours. SAE J1979 carries actual engine percent torque
 * (PID 0x62) and engine friction percent torque (PID 0x8E) as separate
 * standard PIDs, which is exactly indicated-minus-friction, and PID 0x64
 * "engine percent torque data" gives five reference points of which the FIRST
 * IS IDLE -- i.e. the standard also treats the idle value as its own datum
 * rather than a point on a curve. Read off the OBD-II PID tables at
 * en.wikipedia.org/wiki/OBD-II_PIDs and csselectronics.com, which agree; the
 * J1979 document itself is paywalled and has not been read. EVIDENCE, NOT A
 * SPECIFICATION -- the rule above is a decision and stands on its own.
 *
 * Both thresholds are measured off the fixtures, and neither is an equality:
 *
 * SPEED. A stationary car does not send zero. 0x1A0 raw speed is 1 -- i.e.
 * 0.005 km/h -- in every log while standing: 7953 frames in 06_trip_reset,
 * 8002 in 02_idle_60s, 4859 in 17_drive_property_z1. The next value that ever
 * appears is above 40 (0.2 km/h); nothing in between exists in any log. So the
 * gate is a threshold rather than an equality, and 0.1 km/h sits an order of
 * magnitude above the standing value and half an order below the slowest
 * movement ever recorded.
 *
 * THROTTLE. 0x280 b5 reads exactly 38 at rest and 48-61 across the four
 * free-revving holds; 18,060 of 34,495 frames in 17_drive_property_z1 are at
 * 38, and across every fixture in the directory the next value above 38 that
 * ever appears is 44 -- nothing occupies 39 to 43. It is the pedal and not the
 * load, which is why it can gate on its own now: a released pedal is a
 * statement about the driver, and what b7 does afterwards is the engine
 * looking after itself.
 *
 * THE b7 = 133 SPIKE IS NOT A COUNTER-EXAMPLE, though it was once read as one.
 * b7 does reach 133 at throttle 38 in 17_drive_property_z1 -- at 4522 rpm,
 * during a gearchange, in a frame where 0x1A0 was not even reporting a valid
 * speed. It is a transient of the pedal and the load byte disagreeing for a
 * few frames, not a state the car sits in: bucketed by engine speed, mean b7
 * at throttle 38 is 14-17 everywhere above 1000 rpm, which is BELOW the drag
 * line, and only the idle bucket sits above it at 27.6. Gating those spikes
 * away is a second thing this rule buys. */
#define STANDSTILL_MMH          100u        /* 0.1 km/h; standing sends 5   */
#define THROTTLE_REST           38u         /* 0x280 b5 at rest             */

/* Below this the engine is not running, it is being turned by the starter,
 * and b7 stops meaning anything: 06_trip_reset holds b7 = 191-192 through the
 * whole crank, which the model would otherwise show as ~125 Nm and ~9 kW for
 * about half a second at every start. Idle is 797-826 rpm in every fixture, so
 * 500 is clear of anything the running engine does. A DECISION -- no datasheet
 * says where cranking ends. */
#define TORQUE_MIN_RPM          500u

/* power [kW] = torque [Nm] * rpm / 9550, rearranged for the scaled units:
 * power_d [0.1 kW] = torque_cnm * rpm / 95500 */
#define POWER_DIVISOR           95500ul

/* --- persistence -------------------------------------------------------- */

/* Circular buffer in the PIC's 1 kB EEPROM. 64 slots of 12 bytes is 768 B
 * and spreads the wear sixty-four ways. */
#define PERSIST_RECORD_BYTES    12
#define PERSIST_SLOTS           64

/* TWENTY SECONDS, NOT SIXTY. What the interval really sets
 * is how much is thrown away at every ignition-off: the accumulators live in
 * RAM and the stored record is 0 to PERSIST_INTERVAL_MS old, so a switch-off
 * discards half of it on average. persist.h has the full argument; the short
 * version is that the loss is systematic, one-directional, and larger in fuel
 * than in distance, so it biases FuelAvg low.
 *
 * The four intervals costed, on a 600 km / 55 l tankful of sixty journeys
 * (city driving, the pessimistic end) against D120's 100 K writes per byte
 * over 64 slots:
 *
 *   interval   FuelAvg error   endurance, engine-on   at 1 h of driving a day
 *      60 s       -0.51 %            12.2 years              292 years
 *      30 s       -0.26 %             6.1 years              146 years
 *   >> 20 s       -0.17 %             4.1 years               97 years
 *      10 s       -0.09 %             2.0 years               49 years
 *
 * Endurance is not the constraint in any of those rows and never was -- see
 * the D124 note in CLAUDE.md, which is easy to read as tighter than it
 * is. 20 s cuts the error to a sixth of one display digit and still outlasts
 * the car by a factor of five. Below that the returns are deep into what
 * nothing can show.
 *
 * WHAT IT COSTS. Three writes a minute instead of one, so 0.24 % of the time
 * is spent blind behind a 48 ms write instead of 0.08 %, and about 51 frames a
 * minute are dropped instead of 17. All of them are harmless: the fuel counter
 * is absolute so a gap costs nothing, and distance is integrated against the
 * clock rather than against frame arrivals. It also triples the chance that a
 * given switch-off tears a write -- one in 417 rather than one in 1,250 --
 * while cutting what a torn write loses from 60 s to 20, which is a better
 * trade than it first looks.
 *
 * WHAT WAS REJECTED. Writing when the car comes to rest, which sounds like the
 * targeted fix and is not: it would take the distance loss to zero and leave
 * the fuel loss alone, and since FuelAvg is a RATIO whose error is the
 * DIFFERENCE between the two losses, removing one of them makes the displayed
 * average slightly worse (-0.55 % against -0.51 %). It would also be hundreds
 * of writes in a traffic jam. Shortening the interval shrinks both losses
 * together, which is why it is the answer and stopping is not. */
#define PERSIST_INTERVAL_MS     20000u      /* at most three times a minute */

#endif /* CONFIG_H */
