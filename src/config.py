CAMERA_INDEX = 0

# Camera/output resolution
FRAME_WIDTH = 1280
FRAME_HEIGHT = 720

# Lower resolution used for computer-vision processing.
# The final output remains 1280x720.
PROCESS_WIDTH = 640
PROCESS_HEIGHT = 360


# ---------------------------------------------------------
# Cloak colors
# ---------------------------------------------------------

COLOR_RANGES = {
    "blue": {
        "ranges": [
            ((90, 50, 50), (130, 255, 255)),
        ]
    },

    # Red wraps around the HSV hue scale,
    # therefore it needs two ranges.
    "red": {
        "ranges": [
            ((0, 50, 50), (10, 255, 255)),
            ((170, 50, 50), (179, 255, 255)),
        ]
    },

    "green": {
        "ranges": [
            ((35, 50, 50), (85, 255, 255)),
        ]
    },

    "purple": {
        "ranges": [
            ((125, 50, 50), (160, 255, 255)),
        ]
    },
}


DEFAULT_COLOR = "blue"


# ---------------------------------------------------------
# Mask processing
# ---------------------------------------------------------

MORPHOLOGY_KERNEL_SIZE = 5

MASK_EXPANSION = 3

BLUR_KERNEL_SIZE = 7

# Ignore very small detected regions.
MIN_CONTOUR_AREA = 1000


# ---------------------------------------------------------
# Application settings
# ---------------------------------------------------------

BACKGROUND_CAPTURE_SECONDS = 3

# Development mode.
#
# True:
#   Shows Color Mask and Captured Background.
#
# False:
#   Cleaner user-facing experience.
DEBUG = True