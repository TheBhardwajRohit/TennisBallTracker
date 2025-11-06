# Real-Time Tennis Ball Tracker

This project is a real-time object tracker designed to detect and follow a tennis ball in video streams using classic computer vision techniques. It leverages color-based segmentation and a Kalman filter for smooth and robust tracking.

![Tracker Demo](demo_placeholder.png)

*(A sample output showing the tracker in action. The red circle is the raw detection, and the green circle is the smoothed prediction from the Kalman filter.)*

---

## Features

-   **Color-Based Detection:** Uses HSV color space segmentation to isolate the tennis ball from the background, making it robust to minor lighting changes.
-   **Kalman Filter Smoothing:** Implements a Kalman filter to predict the ball's position, smooth its trajectory, and handle brief periods of occlusion or missed detections.
-   **Real-Time Performance:** Optimized for real-time processing on standard hardware.
-   **Configurable:** Easily tune the color detection range to adapt to different video conditions.

---

## Prerequisites

This project is designed to run on an Ubuntu-based system.

-   Ubuntu 20.04+
-   Python 3.8+
-   OpenCV
-   NumPy

---

## Setup and Installation

Follow these steps to set up the project environment.

**1. Update System and Install Dependencies**

Open a terminal and run the following command to ensure your system is up-to-date and install Python and the necessary build tools.

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y python3 python3-pip python3-venv build-essential
```

**2. Clone the Repository (Optional)**

If this project were on Git, you would clone it. For now, just create a project directory.
```bash
mkdir tennis-ball-tracker
cd tennis-ball-tracker
```

**3. Create and Activate a Virtual Environment**

It is highly recommended to use a virtual environment to manage project dependencies.

```bash
# Create the environment
python3 -m venv cv_env

# Activate the environment
source cv_env/bin/activate
```
Your terminal prompt should now be prefixed with `(cv_env)`.

**4. Install Python Packages**

Install the required Python libraries using pip.

```bash
pip install opencv-python numpy
```

---

## Usage

To run the tracker, execute the `track_ball.py` script from your terminal, providing the path to your video file using the `--video` argument.

```bash
python3 track_ball.py --video /path/to/your/video.mp4
```

-   A window will open displaying the video with the tracker running.
-   Press the `q` key to quit the application.

---

## How It Works

The tracking logic follows these steps for each frame of the video:

1.  **Pre-processing:** The frame is blurred to reduce high-frequency noise.
2.  **Color Space Conversion:** The frame is converted from BGR to the HSV (Hue, Saturation, Value) color space, which is more effective for color-based filtering.
3.  **Masking:** A binary mask is created, isolating only the pixels that fall within the pre-defined HSV range for a tennis ball.
4.  **Morphological Operations:** The mask is cleaned using erosion and dilation to remove noise.
5.  **Contour Detection:** The largest contour in the cleaned mask is identified as the ball.
6.  **Kalman Filter Prediction & Update:**
    -   The Kalman filter **predicts** the ball's next position.
    -   If a ball is detected via color, its position is used to **update** and correct the filter's prediction.
    -   The final, smoothed position is drawn on the output frame.

---

## Configuration

The tracker's performance is highly dependent on the HSV color range. If the detection is poor, you may need to adjust these values in `track_ball.py`:

```python
# Adjust these HSV values for your specific video's lighting and ball color
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
```

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.
