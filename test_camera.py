import unittest
from contextlib import redirect_stdout, redirect_stderr
from io import StringIO
from unittest.mock import Mock, patch

import numpy as np

from camera import scan_camera


class CameraTests(unittest.TestCase):
    def run_camera(self, capture, readings):
        output = StringIO()
        with patch("camera.cv2.VideoCapture", return_value=capture), \
             patch("camera.decode_image", side_effect=readings), \
             redirect_stdout(output), redirect_stderr(StringIO()):
            try:
                scan_camera()
            except KeyboardInterrupt:
                pass
        return output.getvalue()

    def test_repeated_frames_print_once_until_label_disappears(self):
        frame = np.zeros((20, 20, 3), dtype=np.uint8)
        capture = Mock()
        capture.read.side_effect = [(True, frame)] * 4 + [KeyboardInterrupt()]
        output = self.run_camera(capture, [["123"], ["123"], [], ["123"]])
        self.assertEqual(output, "123\n123\n")
        capture.release.assert_called_once()

    def test_unavailable_camera_is_released(self):
        capture = Mock()
        capture.isOpened.return_value = False
        with self.assertRaisesRegex(RuntimeError, "Could not open"):
            self.run_camera(capture, [])
        capture.release.assert_called_once()

    def test_failed_frame_is_reported_and_camera_released(self):
        capture = Mock()
        capture.read.return_value = (False, None)
        with self.assertRaisesRegex(RuntimeError, "supplying frames"):
            self.run_camera(capture, [])
        capture.release.assert_called_once()

    def test_decoder_error_still_releases_camera(self):
        capture = Mock()
        capture.read.return_value = (True, np.zeros((20, 20, 3), dtype=np.uint8))
        with self.assertRaisesRegex(ValueError, "decoder failed"):
            self.run_camera(capture, [ValueError("decoder failed")])
        capture.release.assert_called_once()


if __name__ == "__main__":
    unittest.main()
