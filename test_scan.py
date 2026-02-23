import unittest
from io import BytesIO

import barcode
import cv2
import numpy as np
from barcode.writer import ImageWriter

from scan import decode_image


class ScanTests(unittest.TestCase):
    def test_reads_ean13_label(self):
        buffer = BytesIO()
        barcode.get("ean13", "590123412345", writer=ImageWriter()).write(buffer)
        image = cv2.imdecode(np.frombuffer(buffer.getvalue(), np.uint8), cv2.IMREAD_COLOR)
        self.assertEqual(decode_image(image), ["5901234123457"])

    def test_blank_image_has_no_codes(self):
        image = np.full((400, 600, 3), 255, dtype=np.uint8)
        self.assertEqual(decode_image(image), [])


if __name__ == "__main__":
    unittest.main()
