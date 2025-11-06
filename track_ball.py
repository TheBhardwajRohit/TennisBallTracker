# track_ball.py

import argparse
import cv2
import numpy as np

# --- NEW: KALMAN FILTER CLASS ---
class KalmanFilter:
    def __init__(self):
        # State transition matrix (A)
        # We model position and velocity, so it's a 4-state system [x, y, vx, vy]
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        # Transition matrix: defines how the state evolves
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        # Process noise: uncertainty in our model
        self.kf.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.03
    
    def predict(self):
        # Predicts the next state
        return self.kf.predict()

    def update(self, coord):
        # Corrects the state with the new measurement
        return self.kf.correct(coord)

# --- END OF NEW CLASS ---

# Argument parser (no changes)
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video", required=True, help="path to the input video file")
args = vars(ap.parse_args())

# Color range (no changes)
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)

# Load video (no changes)
camera = cv2.VideoCapture(args["video"])
if not camera.isOpened():
    print("Error: Could not open video file.")
    exit()

# --- NEW: INITIALIZE THE KALMAN FILTER ---
kf = KalmanFilter()
predicted_coords = np.zeros((2, 1), np.float32)
# ---

# Main tracking loop
while True:
    (grabbed, frame) = camera.read()
    if not grabbed:
        break

    frame = cv2.resize(frame, (600, 400))
    blurred = cv2.GaussianBlur(frame, (11, 11), 0)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
    mask = cv2.inRange(hsv, greenLower, greenUpper)
    mask = cv2.erode(mask, None, iterations=2)
    mask = cv2.dilate(mask, None, iterations=2)
    
    contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # --- UPDATED LOGIC ---
    # Call predict at the start of each loop
    predicted_coords = kf.predict()

    if len(contours) > 0:
        c = max(contours, key=cv2.contourArea)
        ((x, y), radius) = cv2.minEnclosingCircle(c)
        
        if radius > 10:
            # We have a detection, so update the filter
            measurement = np.array([[np.float32(x)], [np.float32(y)]])
            kf.update(measurement)
            # Draw the raw detection circle in red
            cv2.circle(frame, (int(x), int(y)), int(radius), (0, 0, 255), 2)
    
    # Draw the Kalman filter's predicted position in green
    cv2.circle(frame, (int(predicted_coords[0]), int(predicted_coords[1])), 10, (0, 255, 0), 2)
    # --- END OF UPDATED LOGIC ---

    cv2.imshow("Tennis Ball Tracker", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

camera.release()
cv2.destroyAllWindows()