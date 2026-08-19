#!/usr/bin/env python3
"""Hold a USBtin on the bench bus so that somebody acknowledges the converter.

    python tools/acker.py --port COM8        # until Ctrl-C
    python tools/acker.py --seconds 300      # or for a while

WHY THE BENCH NEEDS THIS, AND THE CAR DOES NOT.

A CAN transmitter needs one other node to pull the acknowledge slot dominant.
On the bench the converter is often the only node with its channel open --
between a flash and the moment a test opens an adapter, nothing acknowledges
anything. So every frame it sends fails, is retransmitted, and its transmit
error counter climbs to the error-passive limit of 128 and stays there: it does
NOT go bus-off and it does NOT fall silent (docs/refuted.md E7). Measured at
1812 frames a second against 22 nominal.

Nothing is damaged by that, and it costs an hour of confusion every time:

  * UNHEALTHY latches, so LED_CAN blinks for the rest of the session and the
    0x603 flag is useless until the next reset
  * the refusal counter saturates at 255, because all three transmit buffers
    are permanently busy
  * both look exactly like a converter with a real fault

Leave this running on the adapter that is not under test and none of it
happens. It transmits nothing itself -- acknowledging is a hardware function of
the CAN controller, not a frame -- so it cannot disturb a measurement.

THE MODE MATTERS AND IT IS THE OPPOSITE OF WHAT IT SOUNDS LIKE. This opens the
channel with `O`, the normal mode. An adapter in listen-only (`L`) is silent in
the acknowledge slot too, which is exactly what 7.4 needs and exactly what is
useless here.

⚠ **It holds the serial port.** 7.3 and 7.4 want two adapters of their own, so
stop this first; 7.1, 7.2 and 7.5 use one and leave the other free for this.
"""

from __future__ import annotations

import argparse
import time

from usbtin_capture import (BITRATE_CMD, CR, command, find_port,
                            require_serial)

try:
    import serial
except ImportError:  # pragma: no cover - depends on the machine
    serial = None


def acknowledge(port: str, seconds: float) -> int:
    """Open the channel and keep it open. Returns the frames seen."""
    require_serial()
    with serial.Serial(port, baudrate=115200, timeout=0.1) as ser:
        # Close first in case a previous run left the channel open, and do not
        # check the answer: a channel that is ALREADY closed answers BEL, so
        # the error here means "nothing to do" as often as it means anything.
        ser.write(b"C" + CR)
        ser.flush()
        time.sleep(0.05)
        ser.reset_input_buffer()

        version = command(ser, b"V", expect_payload=True)
        print(f"USBtin on {port}, firmware "
              f"{version.decode(errors='replace')}")
        command(ser, BITRATE_CMD)
        command(ser, b"O")
        print("channel open at 500 kbit/s in NORMAL mode -- acknowledging, "
              "transmitting nothing")

        seen = 0
        started = time.monotonic()
        reported = started
        try:
            while seconds <= 0 or time.monotonic() - started < seconds:
                chunk = ser.read(4096)
                seen += chunk.count(CR)
                now = time.monotonic()
                if now - reported >= 10.0:
                    reported = now
                    print(f"  {seen} frames acknowledged, "
                          f"{now - started:.0f} s")
        except KeyboardInterrupt:
            print("\nstopping")
        finally:
            command(ser, b"C")
        return seen


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--port", help="serial port (default: autodetect)")
    ap.add_argument("--seconds", type=float, default=0.0,
                    help="stop after this long; 0 means until Ctrl-C")
    args = ap.parse_args(argv)

    port = args.port or find_port()
    seen = acknowledge(port, args.seconds)
    print(f"{seen} frames acknowledged. The converter is on its own again "
          f"from here -- expect UNHEALTHY within a second.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
