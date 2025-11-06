# 🎾 Tennis Ball Tracker GUI

A modern, sleek GUI application for real-time tennis ball detection and tracking using computer vision and Kalman filtering.

## ✨ Features

- **Modern AMOLED-style Dark Interface**: Sleek black design with neon green accents
- **Drag & Drop Video Upload**: Simply drag and drop your video files or browse to select
- **Real-time Processing Animation**: Visual feedback with progress indicators during video analysis
- **Live Tennis Ball Tracking**: Advanced computer vision algorithms detect and track tennis balls
- **Kalman Filter Integration**: Predictive tracking for smooth ball movement estimation
- **Continuous Video Playback**: Videos loop endlessly for continuous analysis
- **Interactive Controls**: Play/pause, restart, and load new videos
- **Enhanced Visualization**: 
  - Orange circles for detected tennis balls
  - Green circles for predicted positions
  - Real-time coordinate display
  - Status indicators and tracking information

## 🚀 Quick Start

### Option 1: Double-click the batch file
```bash
run_gui.bat
```

### Option 2: Run with Python
```bash
python run_gui.py
```

### Option 3: Run directly
```bash
python tennis_ball_tracker_gui_simple.py
```

## 📋 Requirements

The application will automatically check for required dependencies:
- `customtkinter` - Modern UI framework
- `opencv-python` - Computer vision library
- `pillow` - Image processing
- `numpy` - Numerical computations

If any packages are missing, install them with:
```bash
pip install -r requirements_gui.txt
```

## 🎮 How to Use

1. **Launch the Application**: Run the GUI using one of the methods above
2. **Upload Video**: 
   - Drag and drop a video file onto the upload area, or
   - Click "BROWSE FILES" to select a video
3. **Wait for Processing**: The app will show a progress animation while initializing
4. **Watch the Tracking**: Your video will start playing with real-time tennis ball tracking
5. **Use Controls**:
   - **Pause/Play**: Toggle video playback
   - **Restart**: Reset video to beginning
   - **New Video**: Load a different video file

## 📁 Supported Video Formats

- MP4 (recommended)
- AVI
- MOV
- MKV
- WMV
- FLV
- WEBM

## 🔧 Technical Details

### Tennis Ball Detection
- **Color Space**: HSV color filtering for robust detection
- **Range**: Green color range optimized for tennis balls
- **Noise Reduction**: Gaussian blur and morphological operations
- **Contour Detection**: Finds circular objects matching tennis ball characteristics

### Tracking Algorithm
- **Kalman Filter**: 4-state system tracking position and velocity
- **Prediction**: Estimates ball position even when detection fails
- **Correction**: Updates predictions when new detections are available
- **Visualization**: Shows both detected and predicted positions

### GUI Architecture
- **Framework**: CustomTkinter for modern UI components
- **Threading**: Background processing for smooth animation
- **Memory Management**: Efficient video frame processing
- **Error Handling**: Graceful handling of file errors and exceptions

## 🎨 Interface Elements

- **Header**: App title with modern typography
- **Upload Area**: Drag & drop zone with visual feedback
- **Progress Section**: Animated progress bar with status updates
- **Video Display**: Main tracking visualization with enhanced overlays
- **Control Panel**: Playback controls with modern button design
- **Status Indicators**: Real-time tracking status and coordinates

## ⚙️ Configuration

The tennis ball detection parameters can be adjusted in the code:
```python
# HSV color range for tennis ball detection
self.greenLower = (29, 86, 6)
self.greenUpper = (64, 255, 255)
```

## 🐛 Troubleshooting

### Common Issues:

1. **Dependencies Missing**: Run `pip install -r requirements_gui.txt`
2. **Video Won't Load**: Ensure file format is supported
3. **Poor Detection**: Adjust lighting or ball visibility in video
4. **Performance Issues**: Try smaller video resolution

### Error Messages:
- **"Could not open video file"**: File may be corrupted or unsupported format
- **"Failed to initialize video"**: Check file permissions and format

## 🔄 Original vs GUI Comparison

| Feature | Original Script | GUI Version |
|---------|----------------|-------------|
| Interface | Command line | Modern GUI |
| Video Input | Command argument | Drag & drop / Browse |
| Processing | Immediate | Animated progress |
| Controls | Keyboard only | Interactive buttons |
| Visualization | Basic | Enhanced with labels |
| User Experience | Technical | User-friendly |

## 📊 Performance

- **Frame Rate**: ~30 FPS processing
- **Resolution**: Auto-scaled to 800x600 for optimal performance
- **Memory Usage**: Efficient frame-by-frame processing
- **CPU Usage**: Optimized OpenCV operations

## 🛠️ Development

### File Structure:
```
TennisBallTracker/
├── tennis_ball_tracker_gui_simple.py  # Main GUI application
├── run_gui.py                         # Launcher with dependency checks
├── run_gui.bat                        # Windows batch launcher
├── requirements_gui.txt               # GUI-specific dependencies
├── track_ball.py                      # Original command-line version
└── README_GUI.md                      # This file
```

### Extending the Application:
- Add support for multiple ball tracking
- Implement trajectory analysis
- Add video recording capabilities
- Create ball speed calculations
- Implement different sports ball detection

## 📝 License

This project is part of a Digital Image Processing (DIP) course project.

---

**Enjoy tracking tennis balls with style! 🎾✨**