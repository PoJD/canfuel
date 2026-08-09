/* replay_host.c -- run a log through the real C core and print the result.
 *
 * This is the other half of "tools/replay.py --host-build": Python decodes
 * the same log with the reference implementation, this decodes it with the
 * firmware's own decode.c and compute.c, and the two are compared. Any drift
 * between the reference and the thing that will actually be flashed shows up
 * as a failing diff instead of as a wrong number on the display.
 *
 *     ./build/replay_host test/fixtures/02_idle_60s.txt
 *
 * Output is one key=value per line, because it is meant to be parsed.
 */

/* Paths arrive on the command line already complete. */
#define FIXTURE_DIR ""

#include <stdio.h>
#include <string.h>

#include "compute.h"
#include "decode.h"
#include "replay_core.h"
#include "txframes.h"

int main(int argc, char **argv)
{
    int i;

    if (argc < 2) {
        fprintf(stderr, "usage: %s LOG [LOG ...]\n", argv[0]);
        return 2;
    }

    for (i = 1; i < argc; i++) {
        replay_result_t r;
        tx_values_t v;
        uint8_t f600[TXFRAME_DLC], f601[TXFRAME_DLC], f602[TXFRAME_DLC];
        int b;

        if (!replay_log(argv[i], &r)) {
            fprintf(stderr, "replay_host: cannot read %s\n", argv[i]);
            return 1;
        }

        txframes_gather(&v, &r.cp, &r.st, 500, r.cp.last_data_ms);
        txframes_fuel(&v, f600);
        txframes_engine(&v, f601);
        txframes_trip(&v, f602);

        printf("log=%s\n", argv[i]);
        printf("timestamped=%d\n", r.timestamped ? 1 : 0);
        printf("frames=%lu\n", (unsigned long)r.frames);
        printf("fuel_frames=%lu\n", (unsigned long)r.fuel_frames);
        printf("span_ms=%lu\n", (unsigned long)r.span_ms);
        printf("total_ul=%lu\n", (unsigned long)r.cp.total_ul);
        printf("total_mm=%lu\n", (unsigned long)r.cp.total_mm);
        printf("restarts=%lu\n", (unsigned long)r.cp.restarts);
        printf("flow_ul_s=%lu\n", (unsigned long)r.cp.flow_ul_s);
        printf("fuel_now_d=%u\n", v.fuel_now_d);
        printf("fuel_avg_d=%u\n", v.fuel_avg_d);
        printf("tank_d=%u\n", v.fuel_tank_d);
        printf("range_km=%u\n", v.range_km);
        printf("flow_c=%u\n", v.flow_c);
        printf("torque_d=%u\n", v.torque_d);
        printf("power_d=%u\n", v.power_d);

        /* The bytes as they would leave the transceiver, so a mismatch in the
         * layout is visible without a bus analyser. */
        printf("frame_600=");
        for (b = 0; b < TXFRAME_DLC; b++) { printf("%02x", f600[b]); }
        printf("\nframe_601=");
        for (b = 0; b < TXFRAME_DLC; b++) { printf("%02x", f601[b]); }
        printf("\nframe_602=");
        for (b = 0; b < TXFRAME_DLC; b++) { printf("%02x", f602[b]); }
        printf("\n");
    }
    return 0;
}
