/* hal_sys.h -- everything on the PIC that is not the CAN module.
 *
 * HARDWARE. The clock, the ports, the A/D and the EEPROM live behind this
 * header so that decode.c, compute.c, txframes.c and persist.c never have to
 * know which chip they are running on.
 *
 * Sources: DS39977C (PIC18F66K80 family, which is the PIC18F25K80's
 * datasheet). Every constant in hal_sys.c carries its citation.
 */
#ifndef HAL_SYS_H
#define HAL_SYS_H

#include <stdbool.h>
#include <stdint.h>

#include "persist.h"

/* Oscillator, ports, the millisecond timer, the A/D and the interrupt system.
 * Call this first, before anything else in the firmware. It leaves interrupts
 * enabled and the millisecond clock running. */
void hal_sys_init(void);

/* Free-running millisecond counter. It wraps roughly every 49.7 days and the
 * core is built for that -- do not reset it, do not clamp it.
 *
 * Read once at the top of each scheduler pass and hand that one value to every
 * core call in the pass. Reading it again mid-pass can straddle a millisecond
 * and hand compute_tick() a delta of zero where it expects one.
 *
 * The read is atomic against the timer interrupt that writes it. */
uint32_t hal_sys_millis(void);

/* Supply voltage in 0.01 V, measured by the PIC on itself against the internal
 * 1.024 V band gap. This is a trend and a sanity check, not a calibrated
 * voltmeter -- see hal_sys.c for exactly how much it is worth. */
uint16_t hal_sys_vdd_c(void);

/* Is the DBG_EN jumper (JP1, RA0) fitted? The two LEDs are only allowed to
 * light when it is: nothing lights up in the car. Read live, so fitting the
 * jumper takes effect without a reset. */
bool hal_sys_debug_enabled(void);

/* The two LEDs. Both are ignored unless hal_sys_debug_enabled(). */
void hal_sys_led_pwr(bool on);
void hal_sys_led_can(bool on);

/* Clear the watchdog. The main loop calls this once per pass. */
void hal_sys_watchdog_clear(void);

/* --- EEPROM ------------------------------------------------------------- */

/* The two operations persist.c needs, and the backend that wraps them. ctx is
 * unused on the PIC; persist.c passes it through untouched. */
uint8_t hal_eeprom_read(uint16_t addr, void *ctx);
void    hal_eeprom_write(uint16_t addr, uint8_t value, void *ctx);

extern const persist_backend_t hal_eeprom_backend;

#endif /* HAL_SYS_H */
