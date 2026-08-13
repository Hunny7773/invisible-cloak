import cv2
import numpy as np

from config import (
    LOWER_BLUE,
    UPPER_BLUE,
    MORPHOLOGY_KERNEL_SIZE,
    BLUR_KERNEL_SIZE,
)


class CloakProcessor:
    def __init__(self):
        self.lower_blue = np.array(LOWER_BLUE)
        self.upper_blue = np.array(UPPER_BLUE)

        self.kernel = np.ones(
            (
                MORPHOLOGY_KERNEL_SIZE,
                MORPHOLOGY_KERNEL_SIZE,
            ),
            np.uint8,
        )

    def create_mask(self, frame):
        # Convert BGR to HSV
        hsv = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2HSV,
        )

        # Detect blue
        mask = cv2.inRange(
            hsv,
            self.lower_blue,
            self.upper_blue,
        )

        # Remove small noise
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_OPEN,
            self.kernel,
        )

        # Fill small gaps
        mask = cv2.morphologyEx(
            mask,
            cv2.MORPH_CLOSE,
            self.kernel,
        )

        # Smooth mask edges
        mask = cv2.GaussianBlur(
            mask,
            (
                BLUR_KERNEL_SIZE,
                BLUR_KERNEL_SIZE,
            ),
            0,
        )

        return mask

    def create_invisible_effect(
        self,
        frame,
        background,
        mask,
    ):
        # Reverse the mask
        inverse_mask = cv2.bitwise_not(mask)

        # Take cloak area from background
        background_part = cv2.bitwise_and(
            background,
            background,
            mask=mask,
        )

        # Keep everything else from current frame
        current_part = cv2.bitwise_and(
            frame,
            frame,
            mask=inverse_mask,
        )

        # Combine both parts
        result = cv2.add(
            background_part,
            current_part,
        )

        return result