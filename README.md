# 🧥 Invisible Cloak — Python & OpenCV

A real-time computer vision project that creates an "invisible cloak" effect using a webcam, Python, and OpenCV.

The project detects a selected cloak color, creates a binary mask from the detected region, and replaces that region with a previously captured background.

---

## ✨ Features

- Real-time webcam processing
- 1280×720 camera output
- Optimized 640×360 computer-vision processing
- HSV-based color detection
- Multiple cloak colors:
  - 🔵 Blue
  - 🔴 Red
  - 🟢 Green
  - 🟣 Purple
- Three-second background capture countdown
- Background reset
- Cloak pause/resume
- Morphological mask processing
- Contour-based noise filtering
- Mask expansion and smoothing
- FPS monitoring
- Processing-time monitoring
- Debug visualization
- Automated tests with pytest
- Modular project structure

---

## 🧠 How It Works

The project uses a classical computer vision pipeline.

```text
Webcam Frame
     │
     ▼
BGR Image
     │
     ▼
Resize for CV Processing
640 × 360
     │
     ▼
Convert BGR → HSV
     │
     ▼
Color Segmentation
     │
     ▼
Binary Mask
     │
     ▼
Morphological Filtering
     │
     ▼
Contour Filtering
     │
     ▼
Mask Expansion
     │
     ▼
Mask Smoothing
     │
     ▼
Captured Background
     │
     ▼
Invisible Cloak Output