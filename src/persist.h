/* persist.h -- the trip accumulators in EEPROM, in a circular buffer.
 *
 * No hardware in here either. The EEPROM is reached through two function
 * pointers, so hal_sys supplies the real one on the PIC and the tests supply
 * a plain array. That is what makes it possible to simulate a hundred
 * thousand write cycles on a PC in a fraction of a second and check that the
 * wear really is spread.
 *
 * Why a circular buffer at all: the K80's data EEPROM is specified for a
 * minimum of 100 K erase/write cycles per byte (DS39977C Table 31-1, D120;
 * 1000 K typical). Writing one fixed location once a minute would reach that
 * minimum in about 70 days of driving. Sixty-four slots turn it into twelve
 * years, and the sequence number makes a torn write recoverable instead of
 * fatal.
 *
 * A byte write takes 4 ms typical (D122) and blocks, so it must not be done
 * from an interrupt. Once a minute that costs nothing.
 *
 * WHAT EVERY IGNITION-OFF COSTS, AND WHY THE TORN WRITE IS NOT THE
 * INTERESTING CASE.
 *
 * The accumulators live in RAM and reach the EEPROM once a minute, so at any
 * instant the stored record is 0 to 60 s out of date. When the ignition goes
 * off the RAM goes with it, and everything since the last write is gone --
 * uniformly 0 to 60 s, thirty on average. That is not a fault, it is the
 * design; but it is worth stating the right way round, because the obvious
 * reading of the CRC-and-ring machinery above is that losing a minute is the
 * rare bad case. It is not. **Losing a minute is the ordinary case at its
 * maximum**, and a torn write simply pins it there: an unlucky switch-off
 * (about one in 1,250, the 48 ms of writing against the 60 s between) loses
 * 60 s instead of the 30 it would have lost anyway. The lucky switch-off, the
 * one right after a completed write, is the only one that loses nothing.
 *
 * The two accumulators do not lose equally:
 *
 *   fuel      almost always lost. The engine was running, so it was burning:
 *             ~310 ul/s at idle, so 9 ml on an average shutdown.
 *   distance  usually not. The last seconds before a key turn are parking and
 *             idling, so there is often no distance in them at all -- but
 *             switch off the instant the car stops and it can be a kilometre.
 *
 * WHAT IT DOES TO THE NUMBERS. FuelAvg is a ratio and both halves shrink, so
 * it survives: the lost segment does have a higher consumption than the trip
 * average (idling burns fuel and covers no ground), which biases the displayed
 * average LOW -- the gauge flatters the car -- but over a tankful of 20 to 60
 * journeys that is 0.4 to 1.3 % of the fuel against 0.3 to 1 % of the
 * distance, and the ratio moves by **0.1 to 0.3 %**. One digit of the display
 * is 1.4 %. It is invisible.
 *
 * THE ABSOLUTES ARE NOT SO LUCKY. TripFuel and TripDist in 0x602 lose the same
 * fraction with nothing to cancel it, and they lose it in one direction, every
 * shutdown, cumulatively until the next refuelling. They read about half a per
 * cent short of the truth per tankful. Nothing on the display consumes them,
 * but they are exactly what gets compared against a real odometer during
 * bring-up -- so anybody doing that comparison should expect the shortfall and
 * not go looking for an arithmetic bug. docs/frames.md says so too.
 *
 * WHY IT IS NOT FIXED. Writing more often is affordable -- see the endurance
 * arithmetic above; even one write every ten seconds is decades of calendar
 * life -- but it buys nothing anybody can see, because the only consumer that
 * matters is a ratio. Detecting the shutdown in advance would fix it properly
 * and cannot be done: the board is on switched 12 V, so it loses power in the
 * same instant the ECU does, and nothing on the bus arrives early enough to
 * warn us. A hold-up capacitor big enough to finish a record after the rail
 * drops would be a hardware answer to a problem the arithmetic does not have.
 *
 * Record, 12 bytes, little endian:
 *
 *   0-3   total_ul        microlitres since the last reset
 *   4-7   total_mm        millimetres since the last reset
 *   8     tank_stable_l   litres, bit 7 = the value is trustworthy
 *   9     seq             increments per write, wraps at 256
 *   10-11 crc16           CCITT over bytes 0..9
 */
#ifndef PERSIST_H
#define PERSIST_H

#include <stdbool.h>
#include <stdint.h>

#include "config.h"

/* The EEPROM, abstracted down to the two operations that exist. */
typedef struct {
    uint8_t (*read)(uint16_t addr, void *ctx);
    void    (*write)(uint16_t addr, uint8_t value, void *ctx);
    void    *ctx;
} persist_backend_t;

typedef struct {
    uint32_t total_ul;
    uint32_t total_mm;
    uint8_t  tank_stable_l;
    bool     tank_stable_valid;
} persist_record_t;

typedef struct {
    const persist_backend_t *be;
    uint8_t  next_slot;         /* where the next write goes */
    uint8_t  next_seq;
    persist_record_t last;      /* what is already stored, for "only on change" */
    bool     have_last;
    uint32_t last_write_ms;
    bool     have_write_ms;
} persist_t;

/* Find the newest intact record and prepare for the next write.
 *
 * Returns true and fills out when something valid was found. Returns false on
 * a virgin or completely corrupted EEPROM -- out is then zeroed and the
 * caller starts from empty accumulators, which is correct rather than fatal.
 */
bool persist_load(persist_t *p, const persist_backend_t *be,
                  persist_record_t *out);

/* Write, but only if PERSIST_INTERVAL_MS has passed and something actually
 * changed. Returns true when it wrote. This is the one main.c calls. */
bool persist_save(persist_t *p, const persist_record_t *rec, uint32_t now_ms);

/* Write unconditionally. Useful at shutdown and in tests. */
bool persist_save_now(persist_t *p, const persist_record_t *rec);

/* Exposed for the tests. CRC-16/CCITT-FALSE: poly 0x1021, init 0xFFFF. */
uint16_t persist_crc16(const uint8_t *data, uint8_t len);

#endif /* PERSIST_H */
