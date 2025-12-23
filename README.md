# Face Bounding Box Video Tracker

A simple Python script that tracks faces in real-time using your webcam and displays a customizable bounding box with text labels.

## Features

- **Real-time face detection** using OpenCV's Haar Cascade classifier
- **Configurable bounding box color** (green, red, blue, yellow, cyan, magenta, white, orange, purple)
- **Customizable text labels** at the top and bottom of the bounding box
- **Automatic face tracking** that follows detected faces

## Installation

1. Install the required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Basic Usage (with defaults)
```bash
python face_tracker.py
```

This will use:
- **Color**: Green
- **Top Text**: "Face Detected"
- **Bottom Text**: "Tracking Active"

### Custom Configuration

```bash
python face_tracker.py --color red --top-text "Hello!" --bottom-text "Smile :)"
```

### Available Options

- `--camera`: Camera index to use
  - Default: `0` (first camera)
  - Example: `--camera 1` for second camera

- `--list-cameras`: List all available cameras and exit
  - Use this to see which cameras are available on your system

- `--color`: Bounding box color
  - Options: `green`, `red`, `blue`, `yellow`, `cyan`, `magenta`, `white`, `orange`, `purple`
  - Default: `green`

- `--top-text`: Text displayed above the bounding box
  - Default: `"Face Detected"`

- `--bottom-text`: Text displayed below the bounding box
  - Default: `"Tracking Active"`

### Camera Selection

**List available cameras:**
```bash
python face_tracker.py --list-cameras
```

**Use a specific camera:**
```bash
python face_tracker.py --camera 1
```

### Examples

**List all available cameras:**
```bash
python face_tracker.py --list-cameras
```

**Use second camera (index 1):**
```bash
python face_tracker.py --camera 1
```

**Red bounding box with custom text:**
```bash
python face_tracker.py --color red --top-text "Security Camera" --bottom-text "Recording"
```

**Blue bounding box with specific camera:**
```bash
python face_tracker.py --camera 1 --color blue --top-text "User Identified" --bottom-text "Access Granted"
```

**Yellow bounding box:**
```bash
python face_tracker.py --color yellow --top-text "Attention" --bottom-text "Look at camera"
```

## Controls

- Press **'q'** to quit the application

## How It Works

1. The script captures video from your default webcam
2. Each frame is converted to grayscale for face detection
3. OpenCV's Haar Cascade classifier detects faces in the frame
4. For each detected face, a bounding box is drawn with the specified color
5. Text labels are added above and below the bounding box
6. The process repeats in real-time until you press 'q'

## Requirements

- Python 3.7+
- OpenCV (opencv-python)
- A working webcam

## Troubleshooting

**Webcam not opening:**
- Ensure your webcam is connected and not being used by another application
- Check webcam permissions in your system settings

**Face not detected:**
- Ensure adequate lighting
- Face the camera directly
- Move closer to the camera
- The Haar Cascade works best with frontal faces

## License

MIT License
