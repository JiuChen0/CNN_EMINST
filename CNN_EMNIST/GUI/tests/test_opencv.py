import tempfile
import unittest
from pathlib import Path

import cv2
import numpy as np

from CNN.opencv import _active_ranges, segment_characters


class ImageSegmentationTest(unittest.TestCase):
    def test_range_at_image_boundary_is_not_dropped(self):
        self.assertEqual(_active_ranges([0, 2, 2]), [(1, 3)])

    def test_segments_two_characters_into_28_pixel_images(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            image = np.full((120, 240, 3), 255, dtype=np.uint8)
            cv2.putText(
                image,
                "AB",
                (20, 90),
                cv2.FONT_HERSHEY_SIMPLEX,
                2.5,
                (0, 0, 0),
                7,
            )
            source = root / "sample.png"
            cv2.imwrite(str(source), image)

            outputs = segment_characters(source, root / "segments")

            self.assertEqual(len(outputs), 2)
            for output in outputs:
                segmented = cv2.imread(str(output), cv2.IMREAD_GRAYSCALE)
                self.assertEqual(segmented.shape, (28, 28))


if __name__ == "__main__":
    unittest.main()
