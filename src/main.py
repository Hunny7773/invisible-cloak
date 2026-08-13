import time

import cv2

from camera import Camera
from cloak import CloakProcessor

from config import (
    DEFAULT_COLOR,
    DEBUG,
    PROCESS_WIDTH,
    PROCESS_HEIGHT,
    BACKGROUND_CAPTURE_SECONDS,
)


DISPLAY_COLORS = {
    "blue": (255, 0, 0),
    "red": (0, 0, 255),
    "green": (0, 255, 0),
    "purple": (255, 0, 255),
}


COLOR_KEYS = {
    ord("1"): "blue",
    ord("2"): "red",
    ord("3"): "green",
    ord("4"): "purple",
}


def add_status_text(
    image,
    color,
    background_captured,
    cloak_paused,
    fps,
    processing_ms,
    countdown=None,
):
    """Draw application status information on an image."""

    display_color = DISPLAY_COLORS.get(
        color,
        (255, 255, 255),
    )

    if countdown is not None:
        background_status = (
            f"CAPTURING IN: {countdown}"
        )
    elif background_captured:
        background_status = "CAPTURED"
    else:
        background_status = "NOT CAPTURED"

    cloak_status = (
        "PAUSED"
        if cloak_paused
        else "ON"
    )

    cv2.putText(
        image,
        f"Cloak Color: {color.upper()}",
        (20, 35),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        display_color,
        2,
    )

    cv2.putText(
        image,
        f"Background: {background_status}",
        (20, 65),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        image,
        f"Cloak: {cloak_status}",
        (20, 95),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        image,
        f"FPS: {fps:.1f}",
        (20, 125),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )

    cv2.putText(
        image,
        f"Processing: {processing_ms:.1f} ms",
        (20, 155),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2,
    )


def print_controls():
    """Print keyboard controls to the terminal."""

    print()
    print("Controls")
    print("------------------------------")
    print("1 = Blue cloak")
    print("2 = Red cloak")
    print("3 = Green cloak")
    print("4 = Purple cloak")
    print("B = Capture background")
    print("R = Reset background")
    print("SPACE = Pause / Resume cloak")
    print("Q = Quit")
    print("------------------------------")
    print()


def main():
    camera = Camera()

    if not camera.is_opened():
        print(
            "ERROR: Could not open the webcam."
        )
        return

    width, height = camera.get_resolution()

    print(
        f"Camera resolution: "
        f"{width}x{height}"
    )

    print(
        f"Processing resolution: "
        f"{PROCESS_WIDTH}x{PROCESS_HEIGHT}"
    )

    print_controls()

    # -----------------------------------------------------
    # Application state
    # -----------------------------------------------------

    selected_color = DEFAULT_COLOR

    cloak = CloakProcessor(
        selected_color
    )

    background = None

    cloak_paused = False

    capture_start_time = None

    countdown = None

    previous_time = time.perf_counter()

    fps = 0.0

    processing_ms = 0.0

    try:

        while True:

            frame_start = time.perf_counter()

            # -------------------------------------------------
            # Camera
            # -------------------------------------------------

            success, frame = camera.read()

            if not success:
                print(
                    "ERROR: Could not read "
                    "a frame from the webcam."
                )
                break

            # -------------------------------------------------
            # Keyboard
            # -------------------------------------------------

            key = cv2.waitKey(1) & 0xFF

            # -------------------------------------------------
            # Color selection
            # -------------------------------------------------

            if key in COLOR_KEYS:

                selected_color = COLOR_KEYS[key]

                cloak.set_color(
                    selected_color
                )

                print(
                    f"Cloak color: "
                    f"{selected_color.upper()}"
                )

            # -------------------------------------------------
            # Background capture
            # -------------------------------------------------

            if (
                key == ord("b")
                and capture_start_time is None
            ):
                capture_start_time = (
                    time.perf_counter()
                )

                print(
                    "Background capture "
                    "started..."
                )

            # -------------------------------------------------
            # Background countdown
            # -------------------------------------------------

            if capture_start_time is not None:

                elapsed = (
                    time.perf_counter()
                    - capture_start_time
                )

                remaining = (
                    BACKGROUND_CAPTURE_SECONDS
                    - elapsed
                )

                if remaining > 0:

                    countdown = (
                        int(remaining) + 1
                    )

                else:

                    # Capture the current clean frame.
                    background = frame.copy()

                    capture_start_time = None

                    countdown = None

                    print(
                        "Background captured!"
                    )

            # -------------------------------------------------
            # Reset background
            # -------------------------------------------------

            if key == ord("r"):

                background = None

                capture_start_time = None

                countdown = None

                print(
                    "Background reset."
                )

            # -------------------------------------------------
            # Pause / Resume
            # -------------------------------------------------

            if key == 32:

                cloak_paused = (
                    not cloak_paused
                )

                state = (
                    "PAUSED"
                    if cloak_paused
                    else "RESUMED"
                )

                print(
                    f"Cloak {state}."
                )

            # -------------------------------------------------
            # Process frame at lower resolution
            # -------------------------------------------------

            processing_frame = cv2.resize(
                frame,
                (
                    PROCESS_WIDTH,
                    PROCESS_HEIGHT,
                ),
                interpolation=cv2.INTER_AREA,
            )

            # -------------------------------------------------
            # Create mask
            # -------------------------------------------------

            small_mask = cloak.create_mask(
                processing_frame
            )

            # Return mask to output resolution.
            mask = cv2.resize(
                small_mask,
                (width, height),
                interpolation=cv2.INTER_LINEAR,
            )

            # -------------------------------------------------
            # Create cloak effect
            # -------------------------------------------------

            result = None

            if (
                background is not None
                and not cloak_paused
                and capture_start_time is None
            ):

                result = (
                    cloak.create_invisible_effect(
                        frame,
                        background,
                        mask,
                    )
                )

            # -------------------------------------------------
            # Processing metrics
            # -------------------------------------------------

            frame_end = time.perf_counter()

            processing_ms = (
                frame_end - frame_start
            ) * 1000

            current_time = time.perf_counter()

            time_difference = (
                current_time
                - previous_time
            )

            if time_difference > 0:
                fps = (
                    1 / time_difference
                )

            previous_time = current_time

            # -------------------------------------------------
            # Invisible Cloak output
            # -------------------------------------------------

            if result is not None:

                add_status_text(
                    result,
                    selected_color,
                    True,
                    cloak_paused,
                    fps,
                    processing_ms,
                )

                cv2.imshow(
                    "Invisible Cloak",
                    result,
                )

            elif cloak_paused:

                paused_frame = frame.copy()

                add_status_text(
                    paused_frame,
                    selected_color,
                    background is not None,
                    True,
                    fps,
                    processing_ms,
                )

                cv2.imshow(
                    "Invisible Cloak",
                    paused_frame,
                )

            # -------------------------------------------------
            # Camera output
            # -------------------------------------------------

            add_status_text(
                frame,
                selected_color,
                background is not None,
                cloak_paused,
                fps,
                processing_ms,
                countdown,
            )

            cv2.imshow(
                "Camera",
                frame,
            )

            # -------------------------------------------------
            # Debug windows
            # -------------------------------------------------

            if DEBUG:

                cv2.imshow(
                    "Color Mask",
                    mask,
                )

                if background is not None:

                    cv2.imshow(
                        "Captured Background",
                        background,
                    )

            # -------------------------------------------------
            # Quit
            # -------------------------------------------------

            if key == ord("q"):
                break

    except KeyboardInterrupt:

        print(
            "\nApplication interrupted."
        )

    except Exception as error:

        print(
            f"\nUnexpected error: {error}"
        )

    finally:

        camera.release()

        cv2.destroyAllWindows()

        print(
            "Webcam released."
        )

        print(
            "Application closed."
        )


if __name__ == "__main__":
    main()