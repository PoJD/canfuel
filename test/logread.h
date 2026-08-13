/* logread.h -- reads the fixture logs in C. The counterpart of canlog.py.
 *
 * Header only, for the same reason tt.h is: the Makefile compiles one
 * test_*.c against the core and nothing else.
 *
 * Both formats from test/fixtures/README.md are handled:
 *
 *   slcan   t1a0800400100fefe001d          no timestamps
 *   viewer  2078 <TAB> ...png <TAB> 320h <TAB> 8 <TAB> 05 00 86 ...
 *
 * and so is the doubled 02_idle_60s.txt -- see log_load(). The fixture files
 * themselves are never modified; the correction happens at read time exactly
 * as it does in Python.
 */
#ifndef LOGREAD_H
#define LOGREAD_H

#include <stdbool.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#ifndef FIXTURE_DIR
/* Tests are run from test/ by the Makefile. */
#define FIXTURE_DIR "fixtures/"
#endif

/* The USBtin's Z1 timestamp reaches 60000 and the next frame reads 0, so it
 * takes 60001 distinct values. Measured off 08_ign_only_z1.txt, which happens
 * to straddle the restart; the same constant lives in tools/canlog.py as
 * TIMESTAMP_WRAP_MS and the two must not drift apart.
 *
 * Deliberately outside the FIXTURE_DIR guard above: replay_host.c defines
 * FIXTURE_DIR for itself, so anything put inside that block is invisible to
 * exactly the translation unit that needs this most. */
#define LR_TIMESTAMP_WRAP_MS 60001L

typedef struct {
    long     ts_ms;             /* -1 when the format carries no timestamp.
                                 * Unwrapped by log_read(), so it is monotonic
                                 * across the adapter's 60 s restart. */
    uint16_t can_id;
    uint8_t  dlc;
    uint8_t  data[8];
} log_frame_t;

typedef struct {
    log_frame_t *frames;
    size_t       count;
    bool         timestamped;   /* false for slcan, so time must be derived */
} log_file_t;

static inline int lr_hex1(char c)
{
    if (c >= '0' && c <= '9') { return c - '0'; }
    if (c >= 'a' && c <= 'f') { return c - 'a' + 10; }
    if (c >= 'A' && c <= 'F') { return c - 'A' + 10; }
    return -1;
}

static inline int lr_hex2(const char *s)
{
    int hi = lr_hex1(s[0]);
    int lo = lr_hex1(s[1]);
    return (hi < 0 || lo < 0) ? -1 : (hi << 4 | lo);
}

/* Format A: 't' + three hex ID + one hex DLC + two hex chars per byte. */
static inline bool lr_parse_slcan(const char *line, log_frame_t *f)
{
    size_t i;
    int dlc;
    uint16_t id = 0;

    if (line[0] != 't') {
        return false;              /* 'T' is 29 bit and never appears here */
    }
    for (i = 1; i <= 3; i++) {
        int n = lr_hex1(line[i]);
        if (n < 0) { return false; }
        id = (uint16_t)(id << 4 | (unsigned)n);
    }
    dlc = lr_hex1(line[4]);
    if (dlc < 0 || dlc > 8) { return false; }
    if (strlen(line + 5) < (size_t)dlc * 2) { return false; }

    for (i = 0; i < (size_t)dlc; i++) {
        int b = lr_hex2(line + 5 + 2 * i);
        if (b < 0) { return false; }
        f->data[i] = (uint8_t)b;
    }
    /* Opened with Z1 the adapter appends four hex digits of millisecond
     * timestamp after the payload. This parser reads them,
     * when the first Z1 fixtures arrived and log_read() went on synthesising
     * time from an assumed 49.5 ms period instead -- 1583 frames x 49.5 ms is
     * the 78,359 ms it reported for a recording that really ran 60,027.
     *
     * Anything other than exactly four hex digits is treated as no timestamp
     * rather than as a damaged line: the USBtin truncates the final line when
     * the port closes, and losing one frame is better than losing the file. */
    {
        const char *tail = line + 5 + 2 * (size_t)dlc;
        long ts = 0;
        size_t n;
        for (n = 0; n < 4; n++) {
            int v = lr_hex1(tail[n]);
            if (v < 0) { break; }
            ts = ts << 4 | v;
        }
        f->ts_ms = (n == 4 && tail[4] == '\0') ? ts : -1;
    }
    f->can_id = id;
    f->dlc = (uint8_t)dlc;
    return true;
}

/* Format B: five tab separated columns. Rows carrying info.png have empty ID
 * and DLC columns -- they are viewer chatter and are skipped. */
static inline bool lr_parse_viewer(char *line, log_frame_t *f)
{
    char *cols[5];
    char *p = line;
    int n = 0;
    int dlc;
    long id;
    char *end;
    int i;

    while (n < 5) {
        cols[n++] = p;
        p = strchr(p, '\t');
        if (p == NULL) { break; }
        *p++ = '\0';
    }
    if (n < 5) { return false; }
    if (cols[2][0] == '\0' || cols[3][0] == '\0') { return false; }

    id = strtol(cols[2], &end, 16);        /* "320h" -- strtol stops at 'h' */
    if (end == cols[2] || id < 0 || id > 0x7FF) { return false; }
    dlc = (int)strtol(cols[3], &end, 10);
    if (end == cols[3] || dlc < 0 || dlc > 8) { return false; }

    p = cols[4];
    for (i = 0; i < dlc; i++) {
        int b;
        while (*p == ' ') { p++; }
        b = lr_hex2(p);
        if (b < 0) { return false; }
        f->data[i] = (uint8_t)b;
        p += 2;
    }
    f->ts_ms = strtol(cols[0], &end, 10);
    if (end == cols[0]) { f->ts_ms = -1; }
    f->can_id = (uint16_t)id;
    f->dlc = (uint8_t)dlc;
    return true;
}

/* Load a fixture by bare name, e.g. log_load("02_idle_60s.txt", &lf, true).
 *
 * fix_doubled drops the second copy when the file holds the recording exactly
 * twice. 02_idle_60s.txt is damaged that way and without the correction the
 * idle flow comes out at 620 ul/s instead of 310 -- the whole fuel
 * calculation would be off by 100 %.
 */
static inline bool log_load(const char *name, log_file_t *out, bool fix_doubled)
{
    char path[512];
    FILE *fh;
    long size;
    char *buf;
    char **lines;
    size_t nlines = 0, cap = 4096, i;
    size_t used = 0;

    snprintf(path, sizeof path, "%s%s", FIXTURE_DIR, name);
    fh = fopen(path, "rb");
    if (fh == NULL) {
        fprintf(stderr, "logread: cannot open %s\n", path);
        return false;
    }
    fseek(fh, 0, SEEK_END);
    size = ftell(fh);
    fseek(fh, 0, SEEK_SET);
    buf = (char *)malloc((size_t)size + 1);
    lines = (char **)malloc(cap * sizeof *lines);
    if (buf == NULL || lines == NULL) {
        fclose(fh);
        free(buf);
        free(lines);
        return false;
    }
    size = (long)fread(buf, 1, (size_t)size, fh);
    buf[size] = '\0';
    fclose(fh);

    /* Split in place, stripping CR so a Windows checkout compares equal to a
     * Unix one when the doubling is detected. */
    {
        char *p = buf;
        while (p < buf + size) {
            char *nl = strchr(p, '\n');
            char *endl = (nl != NULL) ? nl : buf + size;
            char *cr = endl;
            if (cr > p && cr[-1] == '\r') { cr--; }
            *cr = '\0';
            if (nlines == cap) {
                cap *= 2;
                lines = (char **)realloc(lines, cap * sizeof *lines);
                if (lines == NULL) { free(buf); return false; }
            }
            lines[nlines++] = p;
            if (nl == NULL) { break; }
            p = nl + 1;
        }
    }

    if (fix_doubled && nlines >= 2 && nlines % 2 == 0) {
        size_t half = nlines / 2;
        bool same = true;
        for (i = 0; i < half && same; i++) {
            same = strcmp(lines[i], lines[half + i]) == 0;
        }
        if (same) { nlines = half; }
    }

    out->frames = (log_frame_t *)calloc(nlines ? nlines : 1, sizeof *out->frames);
    if (out->frames == NULL) { free(buf); free(lines); return false; }

    for (i = 0; i < nlines; i++) {
        log_frame_t f;
        bool ok;
        memset(&f, 0, sizeof f);
        if (lines[i][0] == '\0') { continue; }
        ok = (strchr(lines[i], '\t') != NULL)
             ? lr_parse_viewer(lines[i], &f)
             : lr_parse_slcan(lines[i], &f);
        if (ok) {
            out->frames[used++] = f;
        }
        /* A damaged line is skipped, not fatal: the USBtin truncates the last
         * line when the port is closed. */
    }

    out->count = used;
    out->timestamped = used > 0 && out->frames[0].ts_ms >= 0;

    /* Unwrap the adapter's millisecond counter, which runs 0..60000 and then
     * restarts -- measured, see tools/canlog.py TIMESTAMP_WRAP_MS
     * and the note in fixtures/README.md. The counterpart on the Python side
     * is canlog.parse_file(); the two must agree or --host-build diverges on
     * span_ms, which is exactly how this was found.
     *
     * Only a value that goes backwards triggers it, so this is a no-op on
     * USBtinViewer's host timestamps, which pass 60000 without restarting. */
    if (out->timestamped) {
        long offset = 0;
        long previous = -1;
        for (i = 0; i < used; i++) {
            long v = out->frames[i].ts_ms;
            if (v < 0) { continue; }
            if (previous >= 0 && v < previous) { offset += LR_TIMESTAMP_WRAP_MS; }
            previous = v;
            out->frames[i].ts_ms = v + offset;
        }
    }

    free(lines);
    free(buf);
    return used > 0;
}

static inline void log_free(log_file_t *lf)
{
    free(lf->frames);
    lf->frames = NULL;
    lf->count = 0;
}

#endif /* LOGREAD_H */
