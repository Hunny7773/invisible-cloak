import cv2
import numpy as np

from config import (
    COLOR_RANGES,
    DEFAULT_COLOR,
    MORPHOLOGY_KERNEL_SIZE,
    MASK_EXPANSION,
    BLUR_KERNEL_SIZE,
    MIN_CONTOUR_AREA,
)


class CloakProcessor:
    """Handles color detection, mask processing and compositing."""

    def __init__(self, color=DEFAULT_COLOR):
        self.color = color

        self.kernel = np.ones(
            (
                MORPHOLOGY_KERNEL_SIZE,
                MORPHOLOGY_KERNEL_SIZE,
            ),
            dtype=np.uint8,
        )

        self.expansion_kernel = np.ones(
            (
                MASK_EXPANSION,
                MASK_EXPANSION,
            ),
            dtype=np.uint8,
        )

        self.set_color(color)

    def set_color(self, color):
        """Select the cloak color."""
        if color not in COLOR_RANGES:
            raise ValueError(
                f"Unsupported cloak color: {color}"
            )

        self.color = color
        self.use_default_range()

    def use_default_range(self):
        """Load the configured HSV ranges for the current color."""
        ranges = COLOR_RANGES[self.color]["ranges"]

        self.color_ranges = [
            (
                np.array(lower, dtype=np.uint8),
                np.array(upper, dtype=np.uint8),
            )
            for lower, upper in ranges
        ]

    def create_mask(self, frame):
        """
        Create a cleaned binary mask for the selected cloak color.
        """

        if frame is None or frame.size == 0:
            raise ValueError(
                "Invalid frame supplied to create_mask()."
            )

        # BGR -> HSV
        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV,
        )

        # Start with an empty mask.
        mask = np.zeros(
            hsv.shape[:2],
            dtype=np.uint8,
        )

        # Combine all HSV ranges.
        #
        # This is especially important for red because
        # red occupies both ends of the HSV hue scale.
        for lower, upper in self.color_ranges:
            current_mask = cv2.inRange(
                hsv,
                lower,
                upper,
            )

            mask = cv2.bitwise_or(
                mask,
                current_mask,
            )

        # Remove small isolated noise.
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            self.kernel,
        )

        # Fill small holes/gaps.
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            self.kernel,
        )

        # Find connected detected regions.
        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE,
        )

        filtered_mask = np.zeros_like(mask)

        # Remove regions that are too small.
        for contour in contours:
            area = cv2.contourArea(contour)

            if area >= MIN_CONTOUR_AREA:
                cv2.drawContours(
                    filtered_mask,
                    [contour],
                    -1,
                    255,
                    thickness=cv2.FILLED,
                )

        # Slightly expand the mask to reduce tiny gaps
        # around the cloak boundary.
        filtered_mask = cv2.dilate(
            filtered_mask,
            self.expansion_kernel,
            iterations=1,
        )

        # Smooth the final boundary.
        filtered_mask = cv2.GaussianBlur(
            filtered_mask,
            (
                BLUR_KERNEL_SIZE,
                BLUR_KERNEL_SIZE,
            ),
            0,
        )

        return filtered_mask

    def create_invisible_effect(
        self,
        frame,
        background,
        mask,
    ):
        """
        Replace the detected cloak area with the
        corresponding area from the captured background.
        """

        if frame.shape != background.shape:
            raise ValueError(
                "Frame and background dimensions must match."
            )

        if mask.shape[:2] != frame.shape[:2]:
            raise ValueError(
                "Mask dimensions must match the frame."
            )

        inverse_mask = cv2.bitwise_not(mask)

        # Background where cloak is detected.
        background_part = cv2.bitwise_and(
            background,
            background,
            mask=mask,
        )

        # Current camera frame everywhere else.
        current_part = cv2.bitwise_and(
            frame,
            frame,
            mask=inverse_mask,
        )

        # Combine both areas.
        result = cv2.add(
            background_part,
            current_part,
        )

        return result