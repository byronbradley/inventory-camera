import argparse
import sys

import cv2

from scan import decode_image


def scan_camera(device=0, pi=False):
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
                print(value, flush=True)
            previous = values
    finally:
        camera.release()


def main():
    parser = argparse.ArgumentParser(description="Read inventory barcodes from a camera.")
    parser.add_argument("--pi", action="store_true", help="Use a Raspberry Pi CSI camera")
    parser.add_argument("--device", type=int, default=0, help="Camera index (default: 0)")
    args = parser.parse_args()
    try:
        scan_camera(args.device, pi=args.pi)
    except KeyboardInterrupt:
        pass
    except (RuntimeError, cv2.error) as error:
        parser.exit(1, f"{error}\n")


if __name__ == "__main__":
    main()
