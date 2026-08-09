/* test_persist.c -- the EEPROM circular buffer.
 *
 * The two questions worth asking of it are "does the wear really spread" and
 * "what happens when the ignition is pulled halfway through a write". Both
 * are answered here against a RAM array standing in for the EEPROM, which is
 * the entire reason persist.c reaches the memory through function pointers.
 */

#include <string.h>

#include "config.h"
#include "persist.h"
#include "tt.h"

#define EEPROM_BYTES    (PERSIST_SLOTS * PERSIST_RECORD_BYTES)

typedef struct {
    uint8_t  cell[EEPROM_BYTES];
    uint32_t writes[EEPROM_BYTES];      /* cycles used, per byte */
} fake_eeprom_t;

static uint8_t fake_read(uint16_t addr, void *ctx)
{
    fake_eeprom_t *e = (fake_eeprom_t *)ctx;
    return addr < EEPROM_BYTES ? e->cell[addr] : 0xFFu;
}

static void fake_write(uint16_t addr, uint8_t value, void *ctx)
{
    fake_eeprom_t *e = (fake_eeprom_t *)ctx;
    if (addr >= EEPROM_BYTES) {
        return;
    }
    e->cell[addr] = value;
    e->writes[addr]++;
}

static fake_eeprom_t eeprom;
static persist_backend_t backend;

static void eeprom_erase(void)
{
    /* An erased EEPROM on the K80 reads back as 0xFF, not 0x00. */
    memset(eeprom.cell, 0xFF, sizeof eeprom.cell);
    memset(eeprom.writes, 0, sizeof eeprom.writes);
    backend.read = fake_read;
    backend.write = fake_write;
    backend.ctx = &eeprom;
}

static persist_record_t make_rec(uint32_t ul, uint32_t mm, uint8_t tank)
{
    persist_record_t r;
    r.total_ul = ul;
    r.total_mm = mm;
    r.tank_stable_l = tank;
    r.tank_stable_valid = true;
    return r;
}

/* --- the CRC ------------------------------------------------------------ */

static void test_crc_known_vector(void)
{
    /* CRC-16/CCITT-FALSE over "123456789" is 0x29B1. If this ever moves, a
     * record written by an older firmware stops being readable. */
    const uint8_t v[] = "123456789";
    TT_EQ(persist_crc16(v, 9), 0x29B1);
}

/* --- an empty EEPROM ---------------------------------------------------- */

static void test_virgin_eeprom_is_not_an_error(void)
{
    persist_t p;
    persist_record_t out;
    eeprom_erase();
    TT_FALSE(persist_load(&p, &backend, &out));
    /* Starting from empty accumulators is correct, not fatal. */
    TT_EQ(out.total_ul, 0);
    TT_EQ(out.total_mm, 0);
    TT_FALSE(out.tank_stable_valid);
}

/* --- the round trip ----------------------------------------------------- */

static void test_write_then_read_back(void)
{
    persist_t p, q;
    persist_record_t out;
    persist_record_t rec = make_rec(1234567u, 89012345u, 43u);

    eeprom_erase();
    persist_load(&p, &backend, &out);
    TT_TRUE(persist_save_now(&p, &rec));

    /* A fresh persist_t is what a power cycle looks like. */
    TT_TRUE(persist_load(&q, &backend, &out));
    TT_EQ(out.total_ul, rec.total_ul);
    TT_EQ(out.total_mm, rec.total_mm);
    TT_EQ(out.tank_stable_l, rec.tank_stable_l);
    TT_TRUE(out.tank_stable_valid);
}

static void test_invalid_tank_flag_survives(void)
{
    persist_t p, q;
    persist_record_t out;
    persist_record_t rec = make_rec(10u, 20u, 0u);

    eeprom_erase();
    rec.tank_stable_valid = false;
    persist_load(&p, &backend, &out);
    persist_save_now(&p, &rec);
    TT_TRUE(persist_load(&q, &backend, &out));
    TT_FALSE(out.tank_stable_valid);
}

static void test_newest_of_many_wins(void)
{
    persist_t p, q;
    persist_record_t out;
    uint32_t i;

    eeprom_erase();
    persist_load(&p, &backend, &out);
    for (i = 1; i <= 200u; i++) {
        persist_record_t rec = make_rec(i * 1000u, i * 10u, (uint8_t)(i % 60u));
        persist_save_now(&p, &rec);
    }
    TT_TRUE(persist_load(&q, &backend, &out));
    TT_EQ(out.total_ul, 200000u);
    TT_EQ(out.total_mm, 2000u);
}

static void test_sequence_number_wraps(void)
{
    /* The sequence number is one byte, so after 256 writes it starts again.
     * A plain "highest wins" comparison would then pick a record that is
     * nearly a full lap old. */
    persist_t p, q;
    persist_record_t out;
    uint32_t i;

    eeprom_erase();
    persist_load(&p, &backend, &out);
    for (i = 1; i <= 600u; i++) {
        persist_record_t rec = make_rec(i, i * 2u, 10u);
        persist_save_now(&p, &rec);
    }
    TT_TRUE(persist_load(&q, &backend, &out));
    TT_EQ(out.total_ul, 600u);
    TT_EQ(out.total_mm, 1200u);
}

/* --- power loss --------------------------------------------------------- */

static void test_torn_write_falls_back_to_the_previous_record(void)
{
    persist_t p, q;
    persist_record_t out;
    persist_record_t good = make_rec(500000u, 8000000u, 40u);
    persist_record_t torn = make_rec(600000u, 9000000u, 39u);

    eeprom_erase();
    persist_load(&p, &backend, &out);
    persist_save_now(&p, &good);

    /* Now write the next record and pull the ignition halfway through it. */
    {
        uint8_t slot = p.next_slot;
        persist_save_now(&p, &torn);
        eeprom.cell[slot * PERSIST_RECORD_BYTES + 3] ^= 0xFFu;
    }

    TT_TRUE(persist_load(&q, &backend, &out));
    /* The damaged record fails its CRC and the one before it is used. Fuel
     * accounting loses at most one minute, which is what the interval is. */
    TT_EQ(out.total_ul, good.total_ul);
    TT_EQ(out.total_mm, good.total_mm);
}

static void test_a_single_bit_flip_is_caught(void)
{
    persist_t p;
    persist_record_t out;
    persist_record_t rec = make_rec(123456u, 654321u, 33u);
    uint8_t i;

    for (i = 0; i < PERSIST_RECORD_BYTES; i++) {
        eeprom_erase();
        persist_load(&p, &backend, &out);
        persist_save_now(&p, &rec);
        eeprom.cell[i] ^= 0x01u;
        /* One slot written, one bit flipped, nothing else valid anywhere. */
        TT_FALSE(persist_load(&p, &backend, &out));
    }
}

/* --- wear --------------------------------------------------------------- */

static void test_wear_is_spread_evenly_over_100000_cycles(void)
{
    persist_t p;
    persist_record_t out;
    uint32_t i;
    uint32_t min_w = 0xFFFFFFFFu, max_w = 0;
    uint16_t b;

    eeprom_erase();
    persist_load(&p, &backend, &out);
    for (i = 1; i <= 100000u; i++) {
        persist_record_t rec = make_rec(i * 7u, i * 3u, (uint8_t)(i % 60u));
        persist_save_now(&p, &rec);
    }

    for (b = 0; b < EEPROM_BYTES; b++) {
        if (eeprom.writes[b] < min_w) { min_w = eeprom.writes[b]; }
        if (eeprom.writes[b] > max_w) { max_w = eeprom.writes[b]; }
    }
    /* 100,000 writes over 64 slots is 1562.5 each, so every byte must have
     * seen either 1562 or 1563 -- nothing may be favoured. */
    TT_EQ(min_w, 1562u);
    TT_EQ(max_w, 1563u);

    /* And the whole point of the exercise: the K80 is specified for 100,000
     * cycles per byte, so one fixed location would have been used up here
     * while the buffer has spent 1.6 % of its life. */
    TT_TRUE(max_w < 2000u);

    TT_TRUE(persist_load(&p, &backend, &out));
    TT_EQ(out.total_ul, 700000u);
}

/* --- the write policy --------------------------------------------------- */

static void test_save_respects_the_interval(void)
{
    persist_t p;
    persist_record_t out;
    persist_record_t rec = make_rec(1000u, 2000u, 40u);

    eeprom_erase();
    persist_load(&p, &backend, &out);

    TT_TRUE(persist_save(&p, &rec, 0));                     /* first one goes */
    rec.total_ul = 2000u;
    TT_FALSE(persist_save(&p, &rec, PERSIST_INTERVAL_MS - 1u));
    TT_TRUE(persist_save(&p, &rec, PERSIST_INTERVAL_MS));
}

static void test_save_skips_when_nothing_changed(void)
{
    persist_t p;
    persist_record_t out;
    persist_record_t rec = make_rec(1000u, 2000u, 40u);
    uint32_t before;

    eeprom_erase();
    persist_load(&p, &backend, &out);
    persist_save(&p, &rec, 0);
    before = eeprom.writes[0];

    /* Standing at a level crossing with the engine running burns fuel but
     * the accumulator only moves once the counter does. */
    TT_FALSE(persist_save(&p, &rec, PERSIST_INTERVAL_MS));
    TT_FALSE(persist_save(&p, &rec, 10u * PERSIST_INTERVAL_MS));
    TT_EQ(eeprom.writes[0], before);

    rec.total_ul++;
    TT_TRUE(persist_save(&p, &rec, 10u * PERSIST_INTERVAL_MS));
}

int main(void)
{
    printf("test_persist\n");
    TT_RUN(test_crc_known_vector);
    TT_RUN(test_virgin_eeprom_is_not_an_error);
    TT_RUN(test_write_then_read_back);
    TT_RUN(test_invalid_tank_flag_survives);
    TT_RUN(test_newest_of_many_wins);
    TT_RUN(test_sequence_number_wraps);
    TT_RUN(test_torn_write_falls_back_to_the_previous_record);
    TT_RUN(test_a_single_bit_flip_is_caught);
    TT_RUN(test_wear_is_spread_evenly_over_100000_cycles);
    TT_RUN(test_save_respects_the_interval);
    TT_RUN(test_save_skips_when_nothing_changed);
    return TT_SUMMARY();
}
