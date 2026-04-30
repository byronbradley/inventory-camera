# Parts

Selected parts for the planned Pi 3 B+ camera build.

| Qty | Part | Connection / purpose |
| --- | --- | --- |
| 1 | [Raspberry Pi 3 Model B+](https://www.adafruit.com/product/3775) | Runs Raspberry Pi OS, Picamera2, OpenCV, and the barcode decoder |
| 1 | [Camera Module 3, standard colour autofocus](https://www.adafruit.com/product/5657) | Connects to the Pi's CAMERA/CSI socket |
| 1 | 15-pin to 15-pin, 1 mm pitch camera ribbon | Included with Camera Module 3; fits the Pi 3 B+ |
| 1 | [Adafruit 1995, 2.5 A Micro-USB supply](https://www.adafruit.com/product/1995) | Attached cable connects to Pi PWR IN |
| 1 | 128 GB high-endurance microSD card | Raspberry Pi OS and scan logs |
| 1 | microSD reader | OS installation from a computer |
| 1 | Laptop or desktop | OS installation and SSH access over the local network |
| Several | Printed EAN-13 labels with known values | Recognition trials at fixed distances and angles |

Optional: a nonconductive camera mount, Pi case with camera-cable clearance,
and Ethernet cable. Wi-Fi can provide SSH access without Ethernet. A monitor,
HDMI cable, keyboard, and mouse are alternatives to headless setup.

Camera power and data use the CSI ribbon; Pi power uses Micro-USB. These
connections require no breadboard or soldering. Use the 15-to-15-pin ribbon
for the Pi 3 B+.

See [wiring.md](wiring.md) for assembly and connection checks.
