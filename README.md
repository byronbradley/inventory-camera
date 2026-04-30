# Inventory camera

[Pi setup](docs/pi-setup.md) · [Wiring](hardware/wiring.md) · [Parts](hardware/parts.md)

[![Tests](https://github.com/byronbradley/inventory-camera/actions/workflows/tests.yml/badge.svg)](https://github.com/byronbradley/inventory-camera/actions/workflows/tests.yml)

I'm building a Python tool that reads barcodes from inventory labels and logs
them to a CSV file. OpenCV handles the images and
[ZXing-C++](https://github.com/zxing-cpp/zxing-cpp/tree/master/wrappers/python)
reads the barcodes. My code handles retries, repeated readings, camera capture,
and timestamped logging.

So far, I've tested it with generated EAN-13 labels and mocked camera inputs.
The planned build uses a Raspberry Pi 3 B+ and Camera Module 3. I haven't
measured recognition accuracy or frame rate on that hardware yet.

## Run

Use Python 3.12 in a virtual environment:

```sh
python -m pip install -r requirements.txt
python scan.py path/to/label.jpg
python camera.py
```

Use `--device 1` to select another webcam. Readings appear in the terminal;
Ctrl+C stops capture. The [Pi setup](docs/pi-setup.md) covers Camera Module 3.

## What changed after the first tests

The decoder initially read 54 of 60 generated test images correctly. Five
images produced no reading and one produced an extra, incorrect candidate.
I added retries at 2x and 3x image size. When a frame produces more than one
candidate, the code keeps only values also found at 1.5x.

That brought the same set to 60/60, followed by 100/100 on five additional
label values using the same image transformations. These are development
results on generated images, not camera accuracy measurements. The retries
cost processing time, and checking a second scale can discard a real label.

The [experiment notes](docs/recognition-results.md) link the raw results,
commands, and limits of the test images.

## Camera and logging

Laptop and USB cameras use OpenCV. The Pi path uses Picamera2 to capture
1280x720 BGR frames and enables continuous autofocus when available. Neither
path opens a preview window.

By default, readings append to `captures/readings.csv` with the columns
`timestamp_utc,barcode`. To use a separate file:

```sh
python camera.py --output captures/session-1.csv
```

A label is logged once while it is detected in consecutive frames. If a frame
misses it and the next one reads it, it is logged again. The rows count scan
events, not inventory items. Each row is flushed to disk. Use one process per file and import
barcodes as text in spreadsheets so leading zeros survive. Git ignores `captures/`.

## Tests and next steps

```sh
python -m pip install -r requirements-dev.txt
python -m unittest discover -v
```

Tests cover missed and extra readings, repeated labels, UTC timestamps, and
cleanup after camera or file-write failures. Mock cameras check the capture
code without needing a connected device.

The next step is to test printed labels on the Pi at measured distances and
angles, record missed and incorrect reads, and measure frame rate. That will
show how the retries behave with focus, glare, and motion blur.
