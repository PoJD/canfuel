/* persist.h -- the trip accumulators in EEPROM, in a circular buffer.
 *
 * No hardware in here either. The EEPROM is reached through two function
 * pointers, so hal_sys supplies the real one on the PIC and the tests supply
 * a plain array. That is what makes it possible to simulate a hundred
 * thousand write cycles on a PC in a fraction of a second and check that the
 * wear really is spread.
 *
 * Why a circular buffer at all: the K80's EEPROM is specified for 100,000
 * erase/write cycles per byte. Writing one fixed location once a minute would
 * use that up in about 70 days of driving. Sixty-four slots turn that into
 * twelve years, and the sequence number makes a torn write recoverable
 * instead of fatal.
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
