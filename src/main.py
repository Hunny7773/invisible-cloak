import time

import cv2

from camera import Camera
from cloak import CloakProcessor


def main():
    # Create camera
    camera = Camera()

    if not camera.is_opened():
        print("Error: Could not open the webcam.")
        return

    width, height = camera.get_resolution()

    print(f"Camera resolution: {width}x{height}")
    print("Webcam started.")
    print("Press B to capture background.")
    print("Press R to reset background.")
    print("Press Q to quit.")

    # Create cloak processor
    cloak = CloakProcessor()

    # Background starts empty
    background = None

    # FPS variables
    previous_time = time.time()
    fps = 0

    while True:
        # Read webcam frame
        success, frame = camera.read()

        if not success:
            print("Error: Could not read a frame.")
            break

        # Create blue mask
        mask = cloak.create_mask(frame)

        # Read keyboard input
        key = cv2.waitKey(1) & 0xFF

        # Capture background
        if key == ord("b"):
            background = frame.copy()
            print("Background captured!")

        # Reset background
        elif key == ord("r"):
            background = None
            print("Background reset.")

        # Create invisible effect
        if background is not None:
            result = cloak.create_invisible_effect(
                frame,
                background,
                mask,
            )

            cv2.imshow(
                "Invisible Cloak",
                result,
            )

            cv2.imshow(
                "Captured Background",
                background,
            )

            status = (
                "Background: CAPTURED | "
                "B: Recapture | R: Reset | Q: Quit"
            )

        else:
            status = (
                "Background: NOT CAPTURED | "
                "B: Capture | Q: Quit"
            )

        # Calculate FPS
        current_time = time.time()
        time_difference = current_time - previous_time

        if time_difference > 0:
            fps = 1 / time_difference

        previous_time = current_time

        # Display status
        cv2.putText(
            frame,
            status,
            (20, 35),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 0),
            2,
        )

        # Display FPS
        cv2.putText(
            frame,
            f"FPS: {fps:.1f}",
            (20, 70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0, 255, 0),
            2,
        )

        # Show camera
        cv2.imshow(
            "Camera",
            frame,
        )

        # Show mask
        cv2.imshow(
            "Blue Mask",
            mask,
        )

        # Quit
        if key == ord("q"):
            break

    # Clean shutdown
    camera.release()
    cv2.destroyAllWindows()

    print("Webcam stopped.")


if __name__ == "__main__":
    main()