import cv2

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
)



class Camera:
    """Handles webcam input."""

    def __init__(
        self,
        camera_index=CAMERA_INDEX,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
    ):
        self.camera = cv2.VideoCapture(
            camera_index
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width,
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height,
        )

    def is_opened(self):
        """Return True if the webcam opened successfully."""
        return self.camera.isOpened()

    def read(self):
        """Read one frame from the webcam."""
        return self.camera.read()

    def get_resolution(self):
        """Return the actual camera resolution."""
        width = int(
            self.camera.get(
                cv2.CAP_PROP_FRAME_WIDTH
            )
        )

        height = int(
            self.camera.get(
                cv2.CAP_PROP_FRAME_HEIGHT
            )
        )

        return width, height

    def release(self):
        """Release the webcam."""
        if self.camera is not None:
            self.camera.release()