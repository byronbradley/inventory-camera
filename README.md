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

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m unittest -v
```

Tests generate a clean EAN-13 label and a blank image. These check the
image decoder; camera capture and physical lighting/angle trials are next.

## Next

- Add live camera capture.
- Save readings with timestamps.
- Measure recognition across lighting and viewing angles.

OpenCV loads images and converts them to grayscale.
[ZXing-C++](https://github.com/zxing-cpp/zxing-cpp/tree/master/wrappers/python)
decodes the barcodes. OpenCV's built-in decoder did not read the generated
EAN-13 test label, so this version uses ZXing-C++.
