# Face Bounding Box Video Tracker

A simple Python script that tracks faces in real-time using your webcam and displays a customizable bounding box with text labels.

## Features

- **Real-time face detection** using OpenCV's Haar Cascade classifier
- **Configurable bounding box color** (green, red, blue, yellow, cyan, magenta, white, orange, purple)
- **Customizable text labels** at the top and bottom of the bounding box
- **Automatic face tracking** that follows detected faces
- **Smooth bounding box tracking** with configurable frame averaging to reduce jitter
- **Video recording** with keyboard control - press 'r' to start/stop recording
- **Recording indicator** with duration display during recording
- **Multiple camera support** - easily switch between different webcams

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

- `--smoothing-frames`: Number of frames to average for smoothing
  - Default: `5` (higher = smoother but more lag, set to `1` to disable)
  - Recommended range: 3-10 frames

- `--output-dir`: Directory to save recorded videos
  - Default: `recorded_videos`
  - Videos are saved with timestamp filenames (e.g., `face_track_20231223_143052.mp4`)

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

**Disable smoothing for faster response:**
```bash
python face_tracker.py --smoothing-frames 1
```

**High smoothing for very stable box:**
```bash
python face_tracker.py --smoothing-frames 10
```

**Custom output directory for recordings:**
```bash
python face_tracker.py --output-dir "my_recordings"
```

## Controls

- Press **'r'** to start/stop recording
- Press **'q'** to quit the application

## Recording Videos

The script includes built-in video recording functionality:

1. **Start the application** normally
2. **Press 'r'** to start recording - you'll see a red "REC" indicator with a timer
3. **Press 'r' again** to stop recording
4. Videos are automatically saved to the `recorded_videos` folder (or your custom `--output-dir`)
5. Files are named with timestamps: `face_track_YYYYMMDD_HHMMSS.mp4`

**Recording Features:**
- Real-time recording indicator (red circle + "REC" text)
- Duration timer showing recording length (MM:SS)
- Automatic file saving with timestamps
- Records everything including bounding boxes and text overlays

## Smoothing

The bounding box smoothing feature reduces jitter by averaging the position and size over multiple frames:

- **Default smoothing**: 5 frames - good balance between stability and responsiveness
- **More smoothing**: Use `--smoothing-frames 10` for very stable tracking (but slightly more lag)
- **Less smoothing**: Use `--smoothing-frames 3` for faster response to movement
- **No smoothing**: Use `--smoothing-frames 1` to disable (instant response, more jitter)

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
