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
#define CAN_ID_FUEL             0x480u  /* the fuel counter, 49.5 ms        */
#define CAN_ID_ACCEL            0x5A0u  /* acceleration                     */

/* Outgoing, ours. Free on this bus -- see docs/frames.md. */
#define CAN_ID_TX_FUEL          0x600u  /* 100 ms */
#define CAN_ID_TX_ENGINE        0x601u  /* 100 ms */
#define CAN_ID_TX_TRIP          0x602u  /*   1 s  */

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

/* --- timing ------------------------------------------------------------- */

#define PERIOD_FUEL_MS          49      /* nominal period of 0x480, see below */
#define TX_FAST_MS              100     /* 0x600 and 0x601                    */
#define TX_SLOW_MS              1000    /* 0x602 and the EEPROM slot          */
#define RX_POLL_MS              10      /* scheduler slot that drains the CAN */

/* The bus is declared dead after this long without a fuel frame; every
 * transmitted value then goes to zero rather than freezing at its last
 * reading, which would look plausible and be wrong. */
#define DATA_TIMEOUT_MS         500u

/* Sliding window the instantaneous flow is averaged over. At the 49.5 ms
 * period of 0x480 that is roughly twenty samples; the slot count carries
 * headroom for the duplicate frames that make up 39-51 % of every log. */
#define FLOW_WINDOW_MS          1000u
#define FLOW_WINDOW_SLOTS       32

/* --- fuel counter ------------------------------------------------------- */

/* The counter in 0x480 b2-b3 is 15 bits; bit 15 is a wrap flag, not data. */
#define COUNTER_MODULO          32768u
#define COUNTER_MASK            0x7FFFu
#define COUNTER_WRAP_BIT        0x8000u

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

/* --- Range -------------------------------------------------------------- */

/* A rolling average over the last 30 km in 1 km segments, so the estimate
 * falls gradually after a hard pull rather than jumping. */
#define RANGE_SEGMENT_MM        1000000ul   /* 1 km */
#define RANGE_SEGMENTS          30

/* Until this much has been driven the rolling window is too short to trust,
 * so a conservative fixed figure is used instead. */
#define RANGE_MIN_MM            5000000ul   /* 5 km */
#define RANGE_DEFAULT_L100_D    90u         /* 9.0 l/100 km */

/* --- tank level and the refuelling reset -------------------------------- */

/* The instantaneous level is unusable: standing it varies by 2-3 L, driving
 * by 9-10 L because the float sloshes. The median taken at rest is rock
 * solid. docs/refuel-reset.md has the measurements. */
#define TANK_SAMPLE_MS          1000u       /* one sample per second        */
#define TANK_MEDIAN_SLOTS       25          /* so a full median spans 25 s  */
#define TANK_STATIONARY_MMH     1000u       /* "at rest" is below 1 km/h    */

/* The median is trusted from this many samples on, not only from a full
 * window. Refuelling happens with the ignition off, so on the next start the
 * window is empty and the driver may pull away within a few seconds -- with a
 * full window required, the refuelling would never be noticed. Five samples
 * are enough here because the value at rest barely moves: 1584 of 1622
 * measured samples were the same litre. */
#define TANK_MEDIAN_MIN         5

/* A rise of more than this in the stable level means somebody refuelled, and
 * the trip accumulators are cleared. */
#define REFUEL_RISE_L           3u

/* First-order damping of the transmitted tank level, in samples at
 * TANK_SAMPLE_MS -- so this is the time constant in seconds. It feeds both the
 * displayed level and, since 2026-08-11, the range.
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
 * amount of damping makes that reading good. */
#define TANK_DAMP_SAMPLES       120u

/* --- torque and power --------------------------------------------------- */

/* Indicated torque is 0x280 b7, one byte, full scale 255.
 *
 * THE SCALE IS A DECISION, NOT A MEASUREMENT. The ME7 does not send Nm: b7 is
 * a percentage of a reference torque that lives in the ECU's calibration, at
 * ~0.39 % per bit (mfd15/docs/sensors.md §8). Turning that into Nm needs to
 * know what 100 % refers to, and nobody here has that number.
 *
 * This used to be 0.67 Nm/bit, from "the AQY's maximum is 172 Nm, so
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
 * 2026-08-11 and this ECU (06A 906 018 EJ) has no torque measuring block --
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
 * REFITTED 2026-08-11 on the four warm free-revving holds, replacing a line
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
 * THE IDLE POINT IS DELIBERATELY EXCLUDED, AND THE IDLE GATE COVERS IT.
 * 11_idle_noac_z1 is 798 rpm at b7 = 24.96 on the same warm oil, which is ABOVE
 * the line the other four make -- b7 falls 24.96 -> 18.81 between idle and
 * 1536 rpm and only then starts rising. Idle is a different state: the
 * throttle is at its rest position 38 against 48-61 for the holds, so the
 * pumping loss against a nearly closed throttle is large, and the ECU is
 * regulating speed rather than letting the engine free-rev. A straight line in
 * rpm cannot pass through both, so idle is ASSERTED rather than fitted -- see
 * IDLE_GATE_SPEED_MMH below, which returns zero outright for a standing car
 * with the throttle shut. Do not "fix" the residual by raising BASE: that puts
 * the line back above all four measured points and restores the
 * understatement the refit removed, and the gate has already dealt with the
 * only place it showed.
 *
 * STILL NOT HOT. 72-77 C is warm, not the 95-110 C of real driving, so this
 * line very likely still overstates drag a little -- which is the conservative
 * direction. Question 7 in docs/can-decoding.md stays open for exactly that,
 * and is the only open question left. */
#define DRAG_TORQUE_BASE_CNM    674l        /* 6.74 Nm at 0 rpm  (9.11 b7)  */
#define DRAG_TORQUE_SLOPE_E4    4820l       /* 0.4820 cNm per rpm           */

/* THE IDLE GATE. A car that is standing still with the throttle shut is
 * putting out no net torque and no power, and the display says zero. This is
 * A FIXED REQUIREMENT, NOT A CALIBRATION: it holds on cold oil and on hot, at
 * any idle speed the ECU chooses, and it is not to be relaxed or made
 * conditional by any future refit of the drag line. Modern cars behave this
 * way and so does this one. test_compute.c asserts it directly, on every
 * stationary fixture, and test_txframes.c asserts it on the assembled frame.
 *
 * Why it cannot come out of the drag line instead. In neutral the crank drives
 * nothing, so net torque is zero at idle AND at every free-revving hold -- but
 * b7 falls 24.96 -> 18.81 between 798 and 1536 rpm and only then starts
 * rising, because at idle the throttle is nearly shut and the pumping loss is
 * large. No straight line in rpm passes through both, so one of the two has to
 * be asserted rather than fitted. Fitting idle is what the old cold-oil line
 * effectively did, and it understated torque everywhere the car is driven.
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
 * Both thresholds are measured off the fixtures:
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
 * 38. It is the pedal, not the load: b7 reaches 133 at throttle 38 while
 * driving, which is why the throttle ALONE is not a gate and must be paired
 * with the car standing still. Pulling away is throttle > 38 with the car
 * still reading 1, so the gate lets go before the car moves. */
#define IDLE_GATE_SPEED_MMH     100u        /* 0.1 km/h; standing sends 5   */
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
#define PERSIST_INTERVAL_MS     60000u      /* write at most once a minute  */

#endif /* CONFIG_H */
