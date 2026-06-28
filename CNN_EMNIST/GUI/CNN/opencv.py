"""Image segmentation helpers used by the GUI."""

from pathlib import Path
from typing import List, Sequence, Tuple, Union

import cv2
import numpy as np


PathLike = Union[str, Path]
Range = Tuple[int, int]


def _active_ranges(
    projection: Sequence[float], minimum_value: float = 1, minimum_width: int = 2
) -> List[Range]:
    ranges = []
    start = None
    for index, value in enumerate(projection):
        if value > minimum_value and start is None:
            start = index
        elif value <= minimum_value and start is not None:
            if index - start >= minimum_width:
                ranges.append((start, index))
            start = None

    if start is not None and len(projection) - start >= minimum_width:
        ranges.append((start, len(projection)))
    return ranges


def _square_and_resize(image: np.ndarray, padding: int = 4) -> np.ndarray:
    height, width = image.shape
    side = max(height, width) + padding * 2
    canvas = np.zeros((side, side), dtype=np.uint8)
    y = (side - height) // 2
    x = (side - width) // 2
    canvas[y : y + height, x : x + width] = image
    return cv2.resize(canvas, (28, 28), interpolation=cv2.INTER_AREA)


def segment_characters(image_path: PathLike, output_dir: PathLike) -> List[Path]:
    """Split an image into ordered 28x28 character images."""
    source = Path(image_path)
    destination = Path(output_dir)
    destination.mkdir(parents=True, exist_ok=True)
    for old_image in destination.glob("*.png"):
        old_image.unlink()

    image = cv2.imread(str(source))
    if image is None:
        raise ValueError(f"Unable to read image: {source}")

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    threshold = cv2.adaptiveThreshold(
        gray,
        255,
        cv2.ADAPTIVE_THRESH_GAUSSIAN_C,
        cv2.THRESH_BINARY_INV,
        11,
        2,
    )

    # Count foreground pixels rather than summing 0/255 values.
    horizontal_projection = np.count_nonzero(threshold, axis=1)
    line_ranges = _active_ranges(horizontal_projection)
    output_paths = []

    for top, bottom in line_ranges:
        line = threshold[top:bottom, :]
        vertical_projection = np.count_nonzero(line, axis=0)
        character_ranges = _active_ranges(vertical_projection)

        for left, right in character_ranges:
            character = threshold[top:bottom, left:right]
            character = _square_and_resize(character)
            output_path = destination / f"{len(output_paths) + 1}.png"
            if not cv2.imwrite(str(output_path), character):
                raise OSError(f"Unable to write segmented image: {output_path}")
            output_paths.append(output_path)

    return output_paths


# Backwards-compatible name used by the original project.
Images_Processing = segment_characters
