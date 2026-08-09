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

/* Which mode the module runs in. The values are the REQOP<2:0> codes
 * themselves, DS39977C Register 27-1, so that no translation table has to be
 * kept in step with the datasheet.
 *
 * NORMAL is the only one that puts anything on the wire, and it is the only
 * one the finished converter ever uses. The other two exist because the first
 * contact between this firmware and a real 500 kbps bus should not be a node
 * that has already started acknowledging frames:
 *
 *   LISTEN_ONLY  DS39977C §27.3.4: "The Listen Only mode is a silent mode,
 *                meaning no messages will be transmitted while in this state,
 *                including error flags or Acknowledge signals." Receives and
 *                filters exactly as normal. This is what may touch the car
 *                first -- if the bit timing is wrong, a Normal-mode node does
 *                not merely fail to read the bus, it corrupts it with error
 *                frames.
 *
 *   LOOPBACK     DS39977C §27.3.5: transmit buffers are delivered to the
 *                receive buffers "without actually transmitting messages on
 *                the CAN bus ... the device will allow incoming messages from
 *                itself, just as if they were coming from another node", and
 *                it too is silent. The whole transmit and receive path can
 *                therefore be exercised on a bench with no bus attached at
 *                all, and with no transceiver fitted.
 */
typedef enum {
    HAL_CAN_MODE_NORMAL      = 0u,
    HAL_CAN_MODE_LOOPBACK    = 2u,
    HAL_CAN_MODE_LISTEN_ONLY = 3u
} hal_can_mode_t;

/* Bring the module up: pins, 500 kbps bit timing, the seven receive filters,
 * then the requested mode.
 *
 * Returns false if the module never acknowledged a requested mode change. The
 * caller should keep running rather than spinning -- a converter that resets
 * in a loop is worse than one that sits there with a blinking LED. */
bool hal_can_init(hal_can_mode_t mode);

/* True when the mode hal_can_init() reached puts nothing on the bus, i.e.
 * anything but normal -- a diagnostic build, which the caller should say so on
 * an LED. False before hal_can_init() has been called, which is the reset
 * state of REQOP and not worth a special case.
 *
 * There is deliberately no getter for the mode itself. Nothing needs to tell
 * listen-only from loopback at run time, and an accessor nobody calls is a
 * compiler warning on every build. */
bool hal_can_silent(void);

/* Take one frame out of the receive FIFO. Returns false when it is empty.
 * Call it in a loop until it returns false. */
bool hal_can_receive(hal_can_frame_t *frame);

/* Queue one frame. Returns false when all three transmit buffers are still
 * busy, in which case the frame is dropped -- these are periodic frames and
 * the next one is 100 ms away, so a retry queue would only ever transmit
 * stale numbers.
 *
 * In HAL_CAN_MODE_LISTEN_ONLY it queues nothing and returns false without
 * touching the hardware. Setting TXREQ in a mode that never transmits would
 * leave all three buffers permanently busy, which is a worse way to say no
 * than saying no. Loopback does queue, because being delivered to our own
 * receive FIFO is the entire point of it. */
bool hal_can_send(uint16_t id, const uint8_t *data, uint8_t dlc);

/* The two error counters, straight off the module. Worth watching early: the
 * 500 kbps path has been exercised by nobody. */
uint8_t hal_can_rx_errors(void);
uint8_t hal_can_tx_errors(void);

/* True if the module has had to drop a received frame since the last call.
 * Reading it clears the flag. */
bool hal_can_overflow(void);

#endif /* HAL_CAN_H */
