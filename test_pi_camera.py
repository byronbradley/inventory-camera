import sys
import unittest
from unittest.mock import Mock, patch

import numpy as np

from pi_camera import PiCamera


class PiCameraTests(unittest.TestCase):
    def setUp(self):
        self.camera = Mock()
        self.camera.camera_controls = {"AfMode": object()}
        self.picamera = Mock()
        self.picamera.Picamera2.return_value = self.camera
        self.libcamera = Mock()
        self.modules = patch.dict(sys.modules, {
            "picamera2": self.picamera, "libcamera": self.libcamera,
        })
        self.modules.start()
        self.addCleanup(self.modules.stop)

    def test_configures_autofocus_and_returns_bgr_frame(self):
        frame = np.zeros((720, 1280, 3), dtype=np.uint8)
        self.camera.capture_array.return_value = frame
        capture = PiCamera(1)
        self.picamera.Picamera2.assert_called_once_with(camera_num=1)
        self.camera.create_video_configuration.assert_called_once_with(
            main={"size": (1280, 720), "format": "RGB888"}
        )
        self.camera.set_controls.assert_called_once_with({
            "AfMode": self.libcamera.controls.AfModeEnum.Continuous,
        })
        ok, result = capture.read()
        self.assertTrue(ok)
        self.assertIs(result, frame)
        capture.release()
        capture.release()
        self.camera.stop.assert_called_once()
        self.camera.close.assert_called_once()
        self.assertFalse(capture.isOpened())

    def test_configuration_failure_closes_device(self):
        self.camera.configure.side_effect = RuntimeError("configuration failed")
        with self.assertRaisesRegex(RuntimeError, "configuration failed"):
            PiCamera()
        self.camera.close.assert_called_once()

    def test_stop_failure_still_closes_device(self):
        capture = PiCamera()
        self.camera.stop.side_effect = RuntimeError("stop failed")
        with self.assertRaisesRegex(RuntimeError, "stop failed"):
            capture.release()
        self.camera.close.assert_called_once()

    def test_fixed_focus_camera_skips_autofocus(self):
        self.camera.camera_controls = {}
        capture = PiCamera()
        self.camera.set_controls.assert_not_called()
        capture.release()


if __name__ == "__main__":
    unittest.main()
