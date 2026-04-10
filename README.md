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

Each reported reading also appends to `captures/readings.csv` with a UTC
timestamp. Existing rows are kept, with one header. Choose another path with:

```sh
python camera.py --output captures/session-1.csv
python camera.py --pi --output captures/pi-session-1.csv
```

Columns are `timestamp_utc,barcode`. Each row is flushed after writing.
Repeated detections follow the same rule as terminal output above; rows are
scan events, not unique items or inventory quantities. The `captures/` folder
is ignored by Git. Import the barcode column as text in spreadsheets to keep
leading zeros. Use one scanner process per output file.

## Raspberry Pi Camera Module 3

On Raspberry Pi OS Bookworm or newer, install the system camera packages.
Use a separate environment with access to those packages:

```sh
sudo apt update
sudo apt install python3-picamera2 python3-opencv python3-venv
python3 -m venv --system-site-packages .venv-pi
source .venv-pi/bin/activate
python -m pip install zxing-cpp==3.1.1
python camera.py --pi
```

Use the system OpenCV package on the Pi rather than installing the desktop
requirements file into this environment. ZXing wheel availability depends on
the OS/Python version; installation may require a source build.

The Pi path captures 1280x720 BGR frames through Picamera2 and enables continuous
autofocus when supported. `--device` selects the camera index for either backend.
Readings appear in the terminal, including over SSH; Ctrl+C releases the camera.
Connect the ribbon cable with the Pi powered off. If the camera is not detected,
check it with `rpicam-hello --list-cameras` before running the scanner.

## Tests

```sh
python -m pip install -r requirements-dev.txt
python -m unittest -v
```

Tests generate a clean EAN-13 label and a blank image. Camera tests use
simulated frames to check repeated readings, failures, and device cleanup.
Picamera2 tests check configuration, autofocus controls, and cleanup using mocks.
Physical camera trials still need to be run.

## Lighting and viewing angles

```sh
python conditions.py
```

Runs 60 synthetic image trials: three EAN-13 labels, four brightness gains
(0.25, 0.5, 1.0, 1.5), and five horizontal viewing angles (-60, -30, 0, 30, 60
degrees). A pinhole projection simulates a flat label turning around its vertical
axis. Results are saved to [results/synthetic-conditions.csv](results/synthetic-conditions.csv).
`correct` requires exactly the expected barcode with no extra readings.

The current run decoded 57/60 trials exactly, up from the
[54/60 baseline](results/synthetic-conditions-baseline.csv). The decoder retries
empty reads at 2x size and confirms multiple candidates at a second scale.
This recovered two missed reads and removed one extra incorrect candidate.
Three +60-degree trials for `0012345678905` still return no reading.

Retries add processing time; live frame rate has not been measured on the Pi.
Agreement between scales reduces some errors but does not prove a reading is
correct, and confirmation can reject a real label. Results depend on decoder
and image-library versions.

These are generated-image decoder tests. Brightness gain is not a lux measurement,
and projection does not reproduce glare, focus, exposure, motion blur, or sensor
noise. For physical trials, keep distance fixed, measure the label angle, record
the lighting setup, and save frames with known label values. Include failed
reads when calculating the recognition rate.

OpenCV loads images and converts them to grayscale.
[ZXing-C++](https://github.com/zxing-cpp/zxing-cpp/tree/master/wrappers/python)
decodes the barcodes. OpenCV's built-in decoder did not read the generated
EAN-13 test label, so this version uses ZXing-C++.
