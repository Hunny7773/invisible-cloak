import cv2

from config import (
    CAMERA_INDEX,
    FRAME_WIDTH,
    FRAME_HEIGHT,
)


class Camera:
    def __init__(
        self,
        camera_index=CAMERA_INDEX,
        width=FRAME_WIDTH,
        height=FRAME_HEIGHT,
    ):
        self.camera = cv2.VideoCapture(camera_index)

        self.camera.set(
            cv2.CAP_PROP_FRAME_WIDTH,
            width,
        )

        self.camera.set(
            cv2.CAP_PROP_FRAME_HEIGHT,
            height,
        )

    def is_opened(self):
        return self.camera.isOpened()

    def read(self):
        return self.camera.read()

    def get_resolution(self):
        width = int(
            self.camera.get(cv2.CAP_PROP_FRAME_WIDTH)
        )

        height = int(
            self.camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
        )

        return width, height

    def release(self):
        self.camera.release()