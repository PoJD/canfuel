/* hal_can.h -- the ECAN module and the MCP2562 behind it.
 *
 * HARDWARE. 500 kbps, standard 11-bit identifiers only, seven of them accepted
 * by hardware filters and three transmitted.
 *
 * None of this is safe to call from an interrupt: both the receive and the
 * transmit path steer the ECAN access-bank window (ECANCON<4:0>) and would
 * trample each other. The firmware polls, so there is no CAN interrupt to
 * collide with -- see hal_can.c for why polling is enough at this bit rate.
 */
#ifndef HAL_CAN_H
#define HAL_CAN_H

#include <stdbool.h>
#include <stdint.h>

typedef struct {
    uint16_t id;            /* 11-bit standard identifier */
    uint8_t  dlc;           /* 0..8                       */
    uint8_t  data[8];
} hal_can_frame_t;

/* Bring the module up: pins, 500 kbps bit timing, the seven receive filters,
 * then normal mode.
 *
 * Returns false if the module never acknowledged a requested mode change. The
 * caller should keep running rather than spinning -- a converter that resets
 * in a loop is worse than one that sits there with a blinking LED. */
bool hal_can_init(void);

/* Take one frame out of the receive FIFO. Returns false when it is empty.
 * Call it in a loop until it returns false. */
bool hal_can_receive(hal_can_frame_t *frame);

/* Queue one frame. Returns false when all three transmit buffers are still
 * busy, in which case the frame is dropped -- these are periodic frames and
 * the next one is 100 ms away, so a retry queue would only ever transmit
 * stale numbers. */
bool hal_can_send(uint16_t id, const uint8_t *data, uint8_t dlc);

/* The two error counters, straight off the module. Worth watching early: the
 * 500 kbps path has been exercised by nobody. */
uint8_t hal_can_rx_errors(void);
uint8_t hal_can_tx_errors(void);

/* True if the module has had to drop a received frame since the last call.
 * Reading it clears the flag. */
bool hal_can_overflow(void);

#endif /* HAL_CAN_H */
