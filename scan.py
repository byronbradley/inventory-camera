import argparse
from pathlib import Path

import cv2
import zxingcpp


def decode_image(image):
    if image is None or image.size == 0:
        raise ValueError("Image is empty")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    values = _read_values(gray)
    if not values:
        enlarged = cv2.resize(gray, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
        values = _read_values(enlarged)
    if len(values) > 1:
        # Require a second-scale read before reporting multiple candidates.
        check = cv2.resize(gray, None, fx=1.5, fy=1.5, interpolation=cv2.INTER_CUBIC)
        values &= _read_values(check)
    return sorted(values)


def _read_values(gray):
    return {result.text for result in zxingcpp.read_barcodes(gray) if result.valid}


def main():
    parser = argparse.ArgumentParser(description="Read barcodes from an image.")
    parser.add_argument("image", type=Path)
    args = parser.parse_args()
    image = cv2.imread(str(args.image))
    if image is None:
        parser.exit(2, f"Could not read image: {args.image}\n")
    values = decode_image(image)
    for value in values:
        print(value)
    if not values:
        print("No readable barcode found.")


if __name__ == "__main__":
    main()
