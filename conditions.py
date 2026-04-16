import argparse
import csv
from io import BytesIO
from pathlib import Path

import barcode
import cv2
import numpy as np
from barcode.writer import ImageWriter

from scan import decode_image


LABELS = ["590123412345", "400638133393", "001234567890"]
BRIGHTNESS = [0.25, 0.5, 1.0, 1.5]
ANGLES = [-60, -30, 0, 30, 60]


def make_label(value):
    label = barcode.get("ean13", value, writer=ImageWriter())
    buffer = BytesIO()
    label.write(buffer)
    image = cv2.imdecode(np.frombuffer(buffer.getvalue(), np.uint8), cv2.IMREAD_COLOR)
    return image, label.get_fullcode()


def viewing_angle(image, degrees):
    # Project a flat label rotated around its vertical axis through a pinhole camera.
    height, width = image.shape[:2]
    corners = np.float32([[0, 0], [width - 1, 0], [width - 1, height - 1], [0, height - 1]])
    centered = corners - np.float32([(width - 1) / 2, (height - 1) / 2])
    angle = np.deg2rad(degrees)
    focal = 2 * width
    depth = focal - centered[:, 0] * np.sin(angle)
    projected = np.column_stack((
        focal * centered[:, 0] * np.cos(angle) / depth + width,
        focal * centered[:, 1] / depth + height,
    )).astype(np.float32)
    transform = cv2.getPerspectiveTransform(corners, projected)
    return cv2.warpPerspective(image, transform, (2 * width, 2 * height),
                               borderValue=(255, 255, 255))


def run_trials(labels=LABELS):
    rows = []
    for value in labels:
        image, expected = make_label(value)
        for angle in ANGLES:
            tilted = viewing_angle(image, angle)
            for brightness in BRIGHTNESS:
                adjusted = np.clip(tilted.astype(np.float32) * brightness, 0, 255).astype(np.uint8)
                decoded = decode_image(adjusted)
                rows.append({
                    "expected": expected,
                    "brightness_gain": brightness,
                    "yaw_degrees": angle,
                    "decoded": "|".join(decoded),
                    "correct": decoded == [expected],
                })
    return rows


def main():
    parser = argparse.ArgumentParser(description="Run synthetic lighting and viewing-angle trials.")
    parser.add_argument("--output", type=Path, default=Path("results/synthetic-conditions.csv"))
    parser.add_argument("--labels", nargs="+", default=LABELS,
                        help="EAN-13 label values, with or without the check digit")
    args = parser.parse_args()
    rows = run_trials(args.labels)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with args.output.open("w", newline="", encoding="utf-8") as output:
        writer = csv.DictWriter(output, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    correct = sum(row["correct"] for row in rows)
    print(f"Synthetic images: {correct}/{len(rows)} decoded correctly. Results: {args.output}")


if __name__ == "__main__":
    main()
