import sys
from pathlib import Path

import cv2
import numpy as np
import pytest


# Allow imports from src/
SRC_PATH = (
    Path(__file__).resolve().parents[1]
    / "src"
)

sys.path.insert(
    0,
    str(SRC_PATH),
)


from cloak import CloakProcessor
from config import COLOR_RANGES


def create_color_image(
    bgr_color,
    size=(200, 200),
):
    """Create a simple test image with a colored rectangle."""

    image = np.zeros(
        (
            size[1],
            size[0],
            3,
        ),
        dtype=np.uint8,
    )

    cv2.rectangle(
        image,
        (40, 40),
        (160, 160),
        bgr_color,
        thickness=-1,
    )

    return image


def test_supported_colors():
    """All configured colors should be accepted."""

    for color in COLOR_RANGES:
        processor = CloakProcessor(color)

        assert processor.color == color


def test_invalid_color():
    """Invalid colors should raise ValueError."""

    with pytest.raises(ValueError):
        CloakProcessor("orange")


def test_blue_mask_detects_blue():
    """Blue should produce a non-empty mask."""

    processor = CloakProcessor("blue")

    image = create_color_image(
        (255, 0, 0)
    )

    mask = processor.create_mask(
        image
    )

    assert mask.shape == image.shape[:2]

    assert np.count_nonzero(mask) > 0


def test_red_mask_detects_red():
    """Red should be detected using its dual HSV range."""

    processor = CloakProcessor("red")

    image = create_color_image(
        (0, 0, 255)
    )

    mask = processor.create_mask(
        image
    )

    assert mask.shape == image.shape[:2]

    assert np.count_nonzero(mask) > 0


def test_green_mask_detects_green():
    """Green should produce a non-empty mask."""

    processor = CloakProcessor("green")

    image = create_color_image(
        (0, 255, 0)
    )

    mask = processor.create_mask(
        image
    )

    assert np.count_nonzero(mask) > 0


def test_purple_mask_detects_purple():
    """Purple should produce a non-empty mask."""

    processor = CloakProcessor("purple")

    image = create_color_image(
        (255, 0, 255)
    )

    mask = processor.create_mask(
        image
    )

    assert np.count_nonzero(mask) > 0


def test_mask_dimensions():
    """Mask dimensions should match the input frame."""

    processor = CloakProcessor("blue")

    image = np.zeros(
        (300, 400, 3),
        dtype=np.uint8,
    )

    mask = processor.create_mask(
        image
    )

    assert mask.shape == (
        300,
        400,
    )


def test_invisible_effect_dimensions():
    """Output dimensions should match the input frame."""

    processor = CloakProcessor("blue")

    frame = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    background = np.full(
        (100, 100, 3),
        255,
        dtype=np.uint8,
    )

    mask = np.zeros(
        (100, 100),
        dtype=np.uint8,
    )

    mask[25:75, 25:75] = 255

    result = (
        processor.create_invisible_effect(
            frame,
            background,
            mask,
        )
    )

    assert result.shape == frame.shape


def test_invisible_effect_uses_background():
    """Detected mask area should come from the background."""

    processor = CloakProcessor("blue")

    frame = np.zeros(
        (100, 100, 3),
        dtype=np.uint8,
    )

    background = np.full(
        (100, 100, 3),
        255,
        dtype=np.uint8,
    )

    mask = np.zeros(
        (100, 100),
        dtype=np.uint8,
    )

    mask[25:75, 25:75] = 255

    result = (
        processor.create_invisible_effect(
            frame,
            background,
            mask,
        )
    )

    # Center should come from white background.
    center_pixel = result[50, 50]

    assert np.array_equal(
        center_pixel,
        np.array([255, 255, 255]),
    )