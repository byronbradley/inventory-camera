import argparse
from pathlib import Path

import cv2
import zxingcpp


def decode_image(image):
    if image is None or image.size == 0:
        raise ValueError("Image is empty")
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) if image.ndim == 3 else image
    return [result.text for result in zxingcpp.read_barcodes(gray) if result.valid]


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
