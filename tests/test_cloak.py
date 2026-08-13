import sys
from pathlib import Path

import cv2
import numpy as np

# Allow the test file to import modules from src/
sys.path.insert(
    0,
    str(Path(__file__).resolve().parents[1] / "src")
)

from cloak import CloakProcessor


def test_create_mask_detects_blue():
    processor = CloakProcessor()

    # Create a black test image
    image = np.zeros((100, 100, 3), dtype=np.uint8)

    # Add a blue rectangle
    image[25:75, 25:75] = (255, 0, 0)

    # Create mask
    mask = processor.create_mask(image)

    # Make sure the mask contains detected pixels
    assert np.count_nonzero(mask) > 0


def test_create_invisible_effect():
    processor = CloakProcessor()

    # Create two simple images
    frame = np.zeros((100, 100, 3), dtype=np.uint8)
    background = np.full(
        (100, 100, 3),
        255,
        dtype=np.uint8
    )

    # Create a mask
    mask = np.zeros((100, 100), dtype=np.uint8)
    mask[25:75, 25:75] = 255

    # Create invisible effect
    result = processor.create_invisible_effect(
        frame,
        background,
        mask
    )

    # Check that the result has the expected image size
    assert result.shape == frame.shape