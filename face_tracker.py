import cv2
import argparse
import sys
from datetime import datetime
from collections import deque
import os


def list_available_cameras(max_cameras=10):
    """
    List all available cameras and their indices.
    Returns a list of available camera indices.
    """
    available_cameras = []
    print("\n" + "="*50)
    print("Scanning for available cameras...")
    print("="*50)
    
    for i in range(max_cameras):
        cap = cv2.VideoCapture(i)
        if cap.isOpened():
            ret, _ = cap.read()
            if ret:
                available_cameras.append(i)
                # Try to get camera name/backend info
                backend = cap.getBackendName()
                print(f"  Camera {i}: Available (Backend: {backend})")
            cap.release()
    
    if not available_cameras:
        print("  No cameras found!")
    
    print("="*50 + "\n")
    return available_cameras


def main():
    """
    Real-time face tracking with configurable bounding box color and text labels.
    """
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Face tracking with bounding box')
    parser.add_argument('--camera', type=int, default=0,
                        help='Camera index to use (default: 0). Use --list-cameras to see available cameras.')
    parser.add_argument('--list-cameras', action='store_true',
                        help='List all available cameras and exit')
    parser.add_argument('--color', type=str, default='green',
                        help='Bounding box color (green, red, blue, yellow, cyan, magenta, white)')
    parser.add_argument('--top-text', type=str, default='Face Detected',
                        help='Text to display at the top of the bounding box')
    parser.add_argument('--bottom-text', type=str, default='Tracking Active',
                        help='Text to display at the bottom of the bounding box')
    parser.add_argument('--smoothing-frames', type=int, default=5,
                        help='Number of frames to average for smoothing (default: 5, set to 1 to disable)')
    parser.add_argument('--output-dir', type=str, default='recorded_videos',
                        help='Directory to save recorded videos (default: recorded_videos)')
    
    args = parser.parse_args()
    
    # If user wants to list cameras, do that and exit
    if args.list_cameras:
        available = list_available_cameras()
        if available:
            print(f"Found {len(available)} camera(s): {available}")
            print(f"\nTo use a specific camera, run:")
            print(f"  python face_tracker.py --camera <index>")
        return
    
    # Color mapping (BGR format for OpenCV)
    color_map = {
        'green': (0, 255, 0),
        'red': (0, 0, 255),
        'blue': (255, 0, 0),
        'yellow': (0, 255, 255),
        'cyan': (255, 255, 0),
        'magenta': (255, 0, 255),
        'white': (255, 255, 255),
        'orange': (0, 165, 255),
        'purple': (128, 0, 128)
    }
    
    # Get the color from the map, default to green if not found
    box_color = color_map.get(args.color.lower(), (0, 255, 0))
    
    # Load the pre-trained Haar Cascade face detector
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    # Initialize webcam with specified camera index
    print(f"\nAttempting to open camera {args.camera}...")
    cap = cv2.VideoCapture(args.camera)
    
    if not cap.isOpened():
        print(f"\n❌ Error: Could not open camera {args.camera}")
        print("\nTroubleshooting:")
        print("  1. Run with --list-cameras to see available cameras")
        print("  2. Try a different camera index with --camera <index>")
        print("  3. Make sure no other application is using the camera\n")
        sys.exit(1)
    
    # Verify we can actually read from the camera
    ret, _ = cap.read()
    if not ret:
        print(f"\n❌ Error: Camera {args.camera} opened but cannot read frames")
        print("Try a different camera with --camera <index>\n")
        cap.release()
        sys.exit(1)
    
    print(f"✅ Successfully opened camera {args.camera}")
    print("\nFace tracking started.")
    print(f"  Camera Index: {args.camera}")
    print(f"  Box Color: {args.color}")
    print(f"  Top Text: {args.top_text}")
    print(f"  Bottom Text: {args.bottom_text}")
    print(f"  Smoothing: {args.smoothing_frames} frames")
    print("\nControls:")
    print("  Press 'r' to start/stop recording")
    print("  Press 'q' to quit")
    print()
    
    # Recording setup
    is_recording = False
    video_writer = None
    recording_start_time = None
    
    # Create output directory if it doesn't exist
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
        print(f"Created output directory: {args.output_dir}")
    
    # Get frame dimensions for video writer
    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = int(cap.get(cv2.CAP_PROP_FPS)) or 30  # Default to 30 if unable to get FPS
    
    # Smoothing setup - store recent bounding boxes
    bbox_history = deque(maxlen=args.smoothing_frames)
    
    while True:
        # Capture frame-by-frame
        ret, frame = cap.read()
        
        if not ret:
            print("Error: Failed to capture frame")
            break
        
        # Convert to grayscale for face detection
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        
        # Detect faces
        faces = face_cascade.detectMultiScale(
            gray,
            scaleFactor=1.1,
            minNeighbors=5,
            minSize=(30, 30)
        )
        
        # Process detected faces with smoothing
        if len(faces) > 0:
            # Use the first detected face (you can modify to track multiple faces)
            x, y, w, h = faces[0]
            
            # Add to history for smoothing
            bbox_history.append((x, y, w, h))
            
            # Calculate smoothed bounding box (average of recent detections)
            if len(bbox_history) > 0:
                avg_x = int(sum([box[0] for box in bbox_history]) / len(bbox_history))
                avg_y = int(sum([box[1] for box in bbox_history]) / len(bbox_history))
                avg_w = int(sum([box[2] for box in bbox_history]) / len(bbox_history))
                avg_h = int(sum([box[3] for box in bbox_history]) / len(bbox_history))
                
                # Use smoothed values
                x, y, w, h = avg_x, avg_y, avg_w, avg_h
        
        # Draw bounding box and text for detected face
        if len(bbox_history) > 0:
            # Draw rectangle around face
            cv2.rectangle(frame, (x, y), (x + w, y + h), box_color, 2)
            
            # Prepare text settings
            font = cv2.FONT_HERSHEY_SIMPLEX
            font_scale = 0.6
            font_thickness = 2
            
            # Top text
            top_text_size = cv2.getTextSize(args.top_text, font, font_scale, font_thickness)[0]
            top_text_x = x + (w - top_text_size[0]) // 2
            top_text_y = y - 10
            
            # Draw background rectangle for top text
            cv2.rectangle(frame, 
                          (top_text_x - 5, top_text_y - top_text_size[1] - 5),
                          (top_text_x + top_text_size[0] + 5, top_text_y + 5),
                          box_color, -1)
            
            # Draw top text
            cv2.putText(frame, args.top_text, (top_text_x, top_text_y),
                        font, font_scale, (255, 255, 255), font_thickness)
            
            # Bottom text
            bottom_text_size = cv2.getTextSize(args.bottom_text, font, font_scale, font_thickness)[0]
            bottom_text_x = x + (w - bottom_text_size[0]) // 2
            bottom_text_y = y + h + 25
            
            # Draw background rectangle for bottom text
            cv2.rectangle(frame,
                          (bottom_text_x - 5, bottom_text_y - bottom_text_size[1] - 5),
                          (bottom_text_x + bottom_text_size[0] + 5, bottom_text_y + 5),
                          box_color, -1)
            
            # Draw bottom text
            cv2.putText(frame, args.bottom_text, (bottom_text_x, bottom_text_y),
                        font, font_scale, (255, 255, 255), font_thickness)
        
        # Add recording indicator if recording
        if is_recording:
            # Red circle indicator
            cv2.circle(frame, (30, 30), 15, (0, 0, 255), -1)
            cv2.circle(frame, (30, 30), 15, (255, 255, 255), 2)
            
            # REC text
            cv2.putText(frame, "REC", (55, 40), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 0, 255), 2)
            
            # Recording duration
            if recording_start_time:
                duration = (datetime.now() - recording_start_time).total_seconds()
                duration_text = f"{int(duration // 60):02d}:{int(duration % 60):02d}"
                cv2.putText(frame, duration_text, (110, 40), cv2.FONT_HERSHEY_SIMPLEX,
                           0.6, (255, 255, 255), 2)
            
            # Write frame to video file
            if video_writer is not None:
                video_writer.write(frame)
        
        # Display the resulting frame
        cv2.imshow('Face Tracker', frame)
        
        # Handle keyboard input
        key = cv2.waitKey(1) & 0xFF
        
        # Toggle recording with 'r' key
        if key == ord('r'):
            if not is_recording:
                # Start recording
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                output_filename = os.path.join(args.output_dir, f"face_track_{timestamp}.mp4")
                
                # Initialize video writer
                fourcc = cv2.VideoWriter_fourcc(*'mp4v')
                video_writer = cv2.VideoWriter(output_filename, fourcc, fps, 
                                               (frame_width, frame_height))
                
                is_recording = True
                recording_start_time = datetime.now()
                print(f"\n🔴 Recording started: {output_filename}")
            else:
                # Stop recording
                is_recording = False
                if video_writer is not None:
                    video_writer.release()
                    video_writer = None
                print(f"⏹️  Recording stopped")
                recording_start_time = None
        
        # Break loop on 'q' key press
        if key == ord('q'):
            break
    
    # Release resources
    if video_writer is not None:
        video_writer.release()
        print("\n💾 Recording saved")
    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
