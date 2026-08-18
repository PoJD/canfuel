/* persist.c -- see persist.h. No hardware; the EEPROM arrives as two
 * function pointers. */

#include <string.h>

#include "persist.h"

#define REC_LEN         PERSIST_RECORD_BYTES
#define CRC_OFFSET      10
#define TANK_VALID_BIT  0x80u

/* ! NESTED HOT LOOP -- len bytes of eight bits, so 80 iterations for a record.
 * ! It runs once a second inside persist_save() and is the second largest loop
 * ! in the firmware. Read docs/optimisation.md before touching it, and if the
 * ! shape changes, tools/cycles.py has to be told: it costs the inner loop by
 * ! the outer one and will stop rather than guess. */
uint16_t persist_crc16(const uint8_t *data, uint8_t len)
{
    uint16_t crc = 0xFFFFu;
    uint8_t i, bit;

    for (i = 0; i < len; i++) {
        crc ^= (uint16_t)data[i] << 8;
        for (bit = 0; bit < 8u; bit++) {
            crc = (crc & 0x8000u) ? (uint16_t)((crc << 1) ^ 0x1021u)
                                  : (uint16_t)(crc << 1);
        }
    }
    return crc;
}

static void put_le32(uint8_t *p, uint32_t v)
{
    p[0] = (uint8_t)(v & 0xFFu);
    p[1] = (uint8_t)(v >> 8);
    p[2] = (uint8_t)(v >> 16);
    p[3] = (uint8_t)(v >> 24);
}

static uint32_t get_le32(const uint8_t *p)
{
    return (uint32_t)p[0] | (uint32_t)p[1] << 8 |
           (uint32_t)p[2] << 16 | (uint32_t)p[3] << 24;
}

static void encode(uint8_t *buf, const persist_record_t *rec, uint8_t seq)
{
    uint16_t crc;

    put_le32(buf + 0, rec->total_ul);
    put_le32(buf + 4, rec->total_mm);
    /* The tank level really is seven bits -- it comes out of 0x320 b2 masked
     * with 0x7F -- so bit 7 is free to carry the valid flag. That is what
     * makes the record fit in twelve bytes with a full CRC-16. */
    buf[8] = (uint8_t)((rec->tank_stable_l & 0x7Fu) |
                       (rec->tank_stable_valid ? TANK_VALID_BIT : 0u));
    buf[9] = seq;
    crc = persist_crc16(buf, CRC_OFFSET);
    buf[10] = (uint8_t)(crc & 0xFFu);
    buf[11] = (uint8_t)(crc >> 8);
}

static bool decode_rec(const uint8_t *buf, persist_record_t *rec, uint8_t *seq)
{
    uint16_t stored = (uint16_t)(buf[10] | (uint16_t)buf[11] << 8);

    if (stored != persist_crc16(buf, CRC_OFFSET)) {
        return false;
    }
    rec->total_ul = get_le32(buf + 0);
    rec->total_mm = get_le32(buf + 4);
    rec->tank_stable_l = (uint8_t)(buf[8] & 0x7Fu);
    rec->tank_stable_valid = (buf[8] & TANK_VALID_BIT) != 0u;
    *seq = buf[9];
    return true;
}

static void slot_read(const persist_backend_t *be, uint8_t slot, uint8_t *buf)
{
    uint16_t base = (uint16_t)slot * REC_LEN;
    uint8_t i;
    for (i = 0; i < REC_LEN; i++) {
        buf[i] = be->read((uint16_t)(base + i), be->ctx);
    }
}

static void slot_write(const persist_backend_t *be, uint8_t slot,
                       const uint8_t *buf)
{
    uint16_t base = (uint16_t)slot * REC_LEN;
    uint8_t i;
    for (i = 0; i < REC_LEN; i++) {
        be->write((uint16_t)(base + i), buf[i], be->ctx);
    }
}

bool persist_load(persist_t *p, const persist_backend_t *be,
                  persist_record_t *out)
{
    uint8_t slot;
    bool found = false;
    uint8_t best_seq = 0;
    uint8_t best_slot = 0;
    persist_record_t best;

    memset(p, 0, sizeof *p);
    memset(&best, 0, sizeof best);
    memset(out, 0, sizeof *out);
    p->be = be;

    for (slot = 0; slot < PERSIST_SLOTS; slot++) {
        uint8_t buf[REC_LEN];
        persist_record_t rec;
        uint8_t seq;

        slot_read(be, slot, buf);
        if (!decode_rec(buf, &rec, &seq)) {
            continue;           /* virgin, or a write torn by a power loss */
        }
        /* The sequence number wraps at 256, so "newer" is a difference of
         * less than half the range rather than a plain comparison. */
        if (!found || (uint8_t)(seq - best_seq) < 0x80u) {
            found = true;
            best_seq = seq;
            best_slot = slot;
            best = rec;
        }
    }

    if (!found) {
        p->next_slot = 0;
        p->next_seq = 0;
        return false;
    }

    *out = best;
    p->last = best;
    p->have_last = true;
    p->next_slot = (uint8_t)((best_slot + 1u) % PERSIST_SLOTS);
    p->next_seq = (uint8_t)(best_seq + 1u);
    return true;
}

bool persist_save_now(persist_t *p, const persist_record_t *rec)
{
    uint8_t buf[REC_LEN];

    if (p->be == NULL) {
        return false;
    }
    encode(buf, rec, p->next_seq);
    slot_write(p->be, p->next_slot, buf);

    p->next_slot = (uint8_t)((p->next_slot + 1u) % PERSIST_SLOTS);
    p->next_seq = (uint8_t)(p->next_seq + 1u);
    p->last = *rec;
    p->have_last = true;
    return true;
}

/* True for the record a virgin EEPROM produces: all four fields as
 * persist_load() zeroes them when it finds nothing. Restoring it puts the
 * core in exactly the state it is in with no record at all, so storing it
 * carries no information. */
static bool is_empty(const persist_record_t *rec)
{
    return rec->total_ul == 0u && rec->total_mm == 0u &&
           rec->tank_stable_l == 0u && !rec->tank_stable_valid;
}

bool persist_save(persist_t *p, const persist_record_t *rec, uint32_t now_ms)
{
    bool changed;

    if (p->have_write_ms && (uint32_t)(now_ms - p->last_write_ms) < PERSIST_INTERVAL_MS) {
        return false;
    }

    /* Nothing stored and nothing to store. Both gates below are open on the
     * first call after a power-up -- no last write to compare a time against,
     * no last record to compare a value against -- so without this the first
     * slow slot writes a record of zeros onto a virgin part within a second
     * of release from reset, whether or not the engine has ever run. That
     * record is well formed and harmless to read back, but it says exactly
     * what an empty EEPROM already says, and it costs a slot, a write cycle
     * and two kinds of confusion at the bench: an EEData verify against a hex
     * with no EEPROM section fails at address 0, and DIAG_FLAG_PERSIST_OK
     * reads true on a board that has never accumulated anything.
     *
     * The moment either accumulator moves off zero the record stops being
     * empty and the write happens as before, so nothing real is delayed. */
    if (!p->have_last && is_empty(rec)) {
        return false;
    }

    /* Standing at a level crossing with the engine running changes nothing
     * worth a write cycle. */
    changed = !p->have_last ||
              p->last.total_ul != rec->total_ul ||
              p->last.total_mm != rec->total_mm ||
              p->last.tank_stable_l != rec->tank_stable_l ||
              p->last.tank_stable_valid != rec->tank_stable_valid;
    if (!changed) {
        return false;
    }

    if (!persist_save_now(p, rec)) {
        return false;
    }
    p->last_write_ms = now_ms;
    p->have_write_ms = true;
    return true;
}
