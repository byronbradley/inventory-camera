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

    def test_bright_steep_angle_is_retried_at_larger_scale(self):
        for value in ["590123412345", "400638133393"]:
            with self.subTest(label=value):
                image, expected = make_label(value)
                bright = np.clip(viewing_angle(image, 60).astype(np.float32) * 1.5,
                                 0, 255).astype(np.uint8)
                self.assertEqual(decode_image(bright), [expected])

    def test_bright_label_does_not_report_extra_candidate(self):
        image, expected = make_label("001234567890")
        bright = np.clip(viewing_angle(image, 30).astype(np.float32) * 1.5,
                         0, 255).astype(np.uint8)
        self.assertEqual(decode_image(bright), [expected])

    def test_two_separate_labels_are_preserved(self):
        first, first_value = make_label("590123412345")
        second, second_value = make_label("400638133393")
        image = np.concatenate([first, second], axis=0)
        self.assertEqual(decode_image(image), sorted([first_value, second_value]))
