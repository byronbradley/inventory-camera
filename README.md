# Inventory Camera

Python/OpenCV barcode reader for inventory labels.

## Run

Developed with Python 3.12.

```sh
python -m venv .venv
# Activate .venv with the command for your shell.
python -m pip install -r requirements.txt
python scan.py path/to/label.jpg
```

Prints decoded barcode values, or a message when no code can be read.
The first version targets EAN-13 labels.

## Live camera

Connect a USB webcam or use your laptop camera:

```sh
python camera.py
python camera.py --device 1
```

Hold a barcode in view. Readings print in the terminal; there is no preview
window. A label prints once while it stays detected. It can print again after
a frame without that label, so this is not an inventory count. Press Ctrl+C
to stop. Camera-open and frame-read failures exit with an error.

This capture path uses OpenCV webcam devices. The Raspberry Pi Camera Module 3
will need a Picamera2 capture path when we connect it.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m unittest -v
```

Tests generate a clean EAN-13 label and a blank image. Camera tests use
simulated frames to check repeated readings, failures, and device cleanup.
Physical camera and lighting/angle trials still need to be run.

## Next

- Add Picamera2 capture for the Pi Camera Module 3.
- Save readings with timestamps.
- Measure recognition across lighting and viewing angles.

OpenCV loads images and converts them to grayscale.
[ZXing-C++](https://github.com/zxing-cpp/zxing-cpp/tree/master/wrappers/python)
decodes the barcodes. OpenCV's built-in decoder did not read the generated
EAN-13 test label, so this version uses ZXing-C++.
