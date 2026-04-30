# Pi setup

Planned setup: Raspberry Pi 3 B+ with Camera Module 3. These instructions have
not yet been verified on the physical build. See [parts](../hardware/parts.md)
and [wiring](../hardware/wiring.md) for connections.

On Raspberry Pi OS Bookworm or newer:

```sh
sudo apt update
sudo apt install python3-picamera2 python3-opencv python3-venv
python3 -m venv --system-site-packages .venv-pi
source .venv-pi/bin/activate
python -m pip install zxing-cpp==3.1.1
rpicam-hello --list-cameras
python camera.py --pi --output captures/pi-session-1.csv
```

Use system OpenCV in this environment; the desktop requirements file installs
a separate OpenCV build. ZXing installation may require a source build when no
wheel is available for the OS/Python version.

`--device` selects the camera index. Readings appear in the terminal, including
over SSH. Ctrl+C releases the camera. Camera-open and frame-read failures exit
with an error.

Connect the ribbon with power unplugged. If `rpicam-hello --list-cameras` cannot
find the camera, inspect the socket choice, cable orientation, and both latches
before starting the scanner.
