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
 * rating in turn brackets the scale:
 *
 *   85 kW at 5200 rpm   -> 0.745 Nm/bit
 *   170 Nm at 2400 rpm  -> 0.773 Nm/bit
 *
 * 0.75 sits inside that bracket, reproduces both ratings to within 3 % (165 Nm
 * and 85.6 kW), is the same round step VW uses for the two temperature
 * channels in this very frame set, and errs low on torque, which is the
 * conservative direction for a number on a dashboard.
 *
 * What would settle it: a VCDS measuring block against b7, or a full-throttle
 * sniff. Neither exists. test_compute.c pins the ceiling so that a future
 * change cannot quietly put the factory figures out of reach again. */
#define TORQUE_CNM_PER_BIT      75u         /* 0.75 Nm -- see above */

/* Drag torque -- friction, pumps, alternator -- rises with engine speed and
 * is modelled linearly. Both points come out of the fixtures and both are
 * reproduced exactly by the model:
 *
 *   02_idle_60s   797 rpm, b7 = 29 -> 21.75 Nm  (engine driving itself only)
 *   05_rev3000   2940 rpm, b7 = 37 -> 27.75 Nm  (neutral, so no wheel torque)
 *
 *   drag_cnm = BASE + rpm * SLOPE / 10000
 *
 * These are the same two fixture points as ever; only TORQUE_CNM_PER_BIT
 * moved under them, so the line was refitted in the new units. The calibration
 * is in bytes, not Nm -- change the scale and these must be refitted with it,
 * or the model stops passing through its own measurements. */
#define DRAG_TORQUE_BASE_CNM    1952l       /* 19.52 Nm at 0 rpm            */
#define DRAG_TORQUE_SLOPE_E4    2800l       /* 0.2800 cNm per rpm           */

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
