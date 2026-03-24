import argparse
import sys
from contextlib import ExitStack
from pathlib import Path

import cv2

from scan import decode_image
from readings import ReadingLog


def scan_camera(device=0, pi=False, log_path=None):
    with ExitStack() as cleanup:
        log = ReadingLog(log_path) if log_path is not None else None
        if log is not None:
            cleanup.callback(log.close)
        _scan_camera(device, pi, log)


def _scan_camera(device, pi, log):
    if pi:
        from pi_camera import PiCamera
        camera = PiCamera(device)
    else:
        camera = cv2.VideoCapture(device)
    try:
        if not camera.isOpened():
            raise RuntimeError(f"Could not open camera {device}")
        print("Scanning. Press Ctrl+C to stop.", file=sys.stderr)
        previous = set()
        while True:
            ok, frame = camera.read()
            if not ok or frame is None or frame.size == 0:
                raise RuntimeError("Camera stopped supplying frames")
            values = set(decode_image(frame))
            for value in sorted(values - previous):
                if log is not None:
                    log.write(value)
                print(value, flush=True)
            previous = values
    finally:
        camera.release()


def main():
    parser = argparse.ArgumentParser(description="Read inventory barcodes from a camera.")
    parser.add_argument("--pi", action="store_true", help="Use a Raspberry Pi CSI camera")
    parser.add_argument("--device", type=int, default=0, help="Camera index (default: 0)")
    parser.add_argument("--output", type=Path, default=Path("captures/readings.csv"),
                        help="CSV log path (default: captures/readings.csv)")
    args = parser.parse_args()
    try:
        scan_camera(args.device, pi=args.pi, log_path=args.output)
    except KeyboardInterrupt:
        pass
    except (RuntimeError, OSError, ValueError, cv2.error) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
