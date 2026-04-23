# Camera setup parts

Configuration for the Pi camera capture path in this repository.

| Qty | Part | Connection / purpose |
| --- | --- | --- |
| 1 | [Raspberry Pi 3 Model B+](https://www.adafruit.com/product/3775) | Runs Raspberry Pi OS, Picamera2, OpenCV, and the barcode decoder |
| 1 | [Camera Module 3, standard colour autofocus](https://www.adafruit.com/product/5657) | Connects to the Pi's CAMERA/CSI socket |
| 1 | 15-pin to 15-pin, 1 mm pitch camera ribbon | Included with the selected camera; fits the Pi 3 B+ |
| 1 | [5 V-class, 2.5 A Micro-USB power supply](https://www.adafruit.com/product/1995) | Selected Adafruit supply has an attached cable; powers the Pi through PWR IN |
| 1 | 128 GB high-endurance microSD card | Already owned; holds Raspberry Pi OS and scan logs |
| 1 | microSD reader | Already owned; used with a computer to install the OS |
| 1 | Laptop or desktop | OS installation and SSH access over the local network |
| Several | Printed EAN-13 labels with known values | Recognition trials at fixed distances and angles |

Optional: a nonconductive camera mount, Pi case with camera-cable clearance,
and Ethernet cable. Wi-Fi can provide SSH access without Ethernet. A monitor,
HDMI cable, keyboard, and mouse are alternatives to headless setup.

The basic setup uses the CSI ribbon and the Pi power connector. Breadboard,
resistors, jumper wires, and a soldering iron are not needed for these connections.
The separate Micro-USB data cable is not needed when using the selected supply.
Pi Zero/Pi 5 camera adapter cables do not replace the 15-to-15-pin cable here.

See [wiring.md](wiring.md) for assembly and connection checks.
