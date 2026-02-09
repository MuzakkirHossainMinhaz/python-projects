# Camera App

A simple yet feature-rich desktop camera application built with PyQt5 and OpenCV. Capture photos and record videos with a clean, intuitive interface.

## Features

- **Photo Capture**: Take snapshots from your webcam and save them as PNG images
- **Video Recording**: Record videos with pause/resume functionality
- **Smart UI**: Pause button appears only during active recording
- **Timestamped Files**: All captures are automatically named with timestamps to avoid overwrites
- **Resource Management**: Proper cleanup of camera and video writer resources

## Requirements

- Python 3.7+
- PyQt5
- OpenCV (`opencv-contrib-python`)

## Installation

```bash
pip install pyqt5 opencv-contrib-python
```

## Usage

Run the application:

```bash
python main.py
```

### Controls

- **Camera Icon (Top)**: Capture a photo
- **Video Icon (Middle)**: Start/stop video recording
- **Play Icon (Bottom)**: Pause/resume recording (visible only during recording)

All captured photos and videos are saved in the `captures/` directory.

## Project Structure

```
Camera-App/
├── main.py              # Main application file
├── assets/              # Icon assets
│   ├── camera.png
│   ├── video-camera.png
│   ├── pause.png
│   └── stop.png
└── captures/            # Auto-created directory for saved files
```
