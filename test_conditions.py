import unittest

import numpy as np

from conditions import make_label, viewing_angle
from scan import decode_image


class ConditionTests(unittest.TestCase):
    def test_dim_label(self):
        image, expected = make_label("590123412345")
        dimmed = (image.astype(np.float32) * 0.25).astype(np.uint8)
        self.assertEqual(decode_image(dimmed), [expected])

    def test_label_at_moderate_viewing_angles(self):
        image, expected = make_label("001234567890")
        for angle in [-30, 0, 30]:
            with self.subTest(angle=angle):
                self.assertEqual(decode_image(viewing_angle(image, angle)), [expected])

    def test_transformed_blank_image_has_no_readings(self):
        blank = np.full((300, 500, 3), 255, dtype=np.uint8)
        self.assertEqual(decode_image(viewing_angle(blank, 60)), [])
