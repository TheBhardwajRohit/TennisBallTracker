import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import cv2
import numpy as np
import threading
import time
from PIL import Image, ImageTk
import os

# Set the appearance mode and color theme
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

class KalmanFilter:
    def __init__(self):
        self.kf = cv2.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        self.kf.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) * 0.03
    
    def predict(self):
        return self.kf.predict()

    def update(self, coord):
        return self.kf.correct(coord)

class TennisBallTrackerGUI:
    def __init__(self):
        # Initialize the main window
        self.root = ctk.CTk()
        self.root.title("Tennis Ball Tracker")
        self.root.geometry("1200x900")
        self.root.configure(bg="#000000")
        
        # Modern Formal Color Scheme
        self.colors = {
            "bg_primary": "#000000",        # Pure black background
            "bg_secondary": "#14213d",      # Dark blue for cards/panels
            "bg_tertiary": "#1a2a4d",       # Lighter blue variant
            "accent": "#fca311",            # Orange accent
            "accent_hover": "#e59400",      # Darker orange for hover
            "accent_secondary": "#ffffff",  # White secondary accent
            "text_primary": "#ffffff",      # White text
            "text_secondary": "#e5e5e5",    # Light gray text
            "text_tertiary": "#b0b0b0",     # Medium gray text
            "border": "#2a3a5d",            # Blue-gray divider
            "success": "#00C853",           # Success state (green)
            "warning": "#fca311",           # Warning state (orange)
            "error": "#FF3D00",             # Error state (red)
            "detected": "#fca311",          # Orange for detected ball
            "predicted": "#00C853"          # Green for predicted position
        }
        
        # Initialize variables
        self.video_path = None
        self.video_cap = None
        self.is_playing = False
        self.current_frame = None
        self.kf = None
        self.processing_complete = False
        
        # Tennis ball detection parameters
        self.greenLower = (29, 86, 6)
        self.greenUpper = (64, 255, 255)
        
        self.setup_ui()
        
    def setup_ui(self):
        # Main container with gradient effect
        self.main_frame = ctk.CTkFrame(
            self.root, 
            fg_color=self.colors["bg_primary"],
            corner_radius=0
        )
        self.main_frame.pack(fill="both", expand=True)
        
        # Header section with formal dark blue styling
        self.header_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_secondary"],
            height=100,
            corner_radius=15
        )
        self.header_frame.pack(fill="x", padx=30, pady=(30, 20))
        self.header_frame.pack_propagate(False)
        
        # Title with orange accent
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="🎾 TENNIS BALL TRACKER",
            font=ctk.CTkFont(size=36, weight="bold"),
            text_color=self.colors["accent"]
        )
        self.title_label.pack(expand=True)
        
        self.subtitle_label = ctk.CTkLabel(
            self.header_frame,
            text="AI-Powered Real-time Tennis Ball Detection & Tracking",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        )
        self.subtitle_label.pack()
        
        # Upload section with formal dark blue styling
        self.upload_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_secondary"],
            border_width=2,
            border_color=self.colors["border"],
            height=250,
            corner_radius=15
        )
        self.upload_frame.pack(fill="x", padx=30, pady=(0, 20))
        self.upload_frame.pack_propagate(False)
        
        # Upload content with hover effect
        self.upload_content_frame = ctk.CTkFrame(
            self.upload_frame, 
            fg_color="transparent"
        )
        self.upload_content_frame.pack(expand=True, fill="both", padx=30, pady=30)
        
        # Upload icon with orange accent
        self.upload_icon_label = ctk.CTkLabel(
            self.upload_content_frame,
            text="📁",
            font=ctk.CTkFont(size=64),
            text_color=self.colors["accent"]
        )
        self.upload_icon_label.pack(pady=(20, 15))
        
        # Upload text with better styling
        self.upload_text_label = ctk.CTkLabel(
            self.upload_content_frame,
            text="DRAG & DROP YOUR VIDEO FILE HERE",
            font=ctk.CTkFont(size=18, weight="bold"),
            text_color=self.colors["text_primary"]
        )
        self.upload_text_label.pack(pady=(0, 5))
        
        self.upload_subtext_label = ctk.CTkLabel(
            self.upload_content_frame,
            text="Supports any format that OpenCV can handle (MP4, AVI, MOV, MKV, WMV, etc.)",
            font=ctk.CTkFont(size=12),
            text_color=self.colors["text_secondary"]
        )
        self.upload_subtext_label.pack(pady=(0, 15))
        
        # Modern browse button with orange accent
        self.browse_button = ctk.CTkButton(
            self.upload_content_frame,
            text="🔍 BROWSE FILES",
            command=self.browse_file,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#000000",
            font=ctk.CTkFont(size=16, weight="bold"),
            height=45,
            width=200,
            corner_radius=25
        )
        self.browse_button.pack(pady=(0, 20))
        
        # Make upload area clickable
        def on_upload_click(event):
            self.browse_file()
        
        self.upload_frame.bind("<Button-1>", on_upload_click)
        self.upload_content_frame.bind("<Button-1>", on_upload_click)
        
        # Progress section with formal styling
        self.progress_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_secondary"],
            height=150,
            corner_radius=15
        )
        
        self.progress_title_label = ctk.CTkLabel(
            self.progress_frame,
            text="🔄 PROCESSING VIDEO",
            font=ctk.CTkFont(size=24, weight="bold"),
            text_color=self.colors["accent"]
        )
        self.progress_title_label.pack(pady=(25, 10))
        
        self.progress_bar = ctk.CTkProgressBar(
            self.progress_frame,
            width=500,
            height=25,
            progress_color=self.colors["accent"],
            fg_color=self.colors["border"],
            corner_radius=15
        )
        self.progress_bar.pack(pady=(0, 10))
        self.progress_bar.set(0)
        
        self.progress_status_label = ctk.CTkLabel(
            self.progress_frame,
            text="Initializing AI detection algorithms...",
            font=ctk.CTkFont(size=14),
            text_color=self.colors["text_secondary"]
        )
        self.progress_status_label.pack(pady=(0, 25))
        
        # Video display section with orange border
        self.video_frame = ctk.CTkFrame(
            self.main_frame,
            fg_color=self.colors["bg_secondary"],
            border_width=3,
            border_color=self.colors["accent"],
            corner_radius=15
        )
        
        # Video title
        self.video_title_frame = ctk.CTkFrame(
            self.video_frame,
            fg_color="transparent",
            height=50
        )
        self.video_title_frame.pack(fill="x", padx=20, pady=(20, 10))
        self.video_title_frame.pack_propagate(False)
        
        self.video_title_label = ctk.CTkLabel(
            self.video_title_frame,
            text="🎯 LIVE TRACKING ANALYSIS",
            font=ctk.CTkFont(size=20, weight="bold"),
            text_color=self.colors["accent"]
        )
        self.video_title_label.pack(side="left")
        
        self.tracking_status_label = ctk.CTkLabel(
            self.video_title_frame,
            text="● ACTIVE",
            font=ctk.CTkFont(size=12, weight="bold"),
            text_color=self.colors["success"]
        )
        self.tracking_status_label.pack(side="right")
        
        # Video display area
        self.video_display_frame = ctk.CTkFrame(
            self.video_frame,
            fg_color=self.colors["bg_primary"],
            corner_radius=15
        )
        self.video_display_frame.pack(fill="both", expand=True, padx=20, pady=(0, 10))
        
        self.video_label = ctk.CTkLabel(
            self.video_display_frame,
            text="",
            fg_color="transparent"
        )
        self.video_label.pack(expand=True, padx=10, pady=10)
        
        # Control panel with modern buttons
        self.control_frame = ctk.CTkFrame(
            self.video_frame, 
            fg_color="transparent",
            height=70
        )
        self.control_frame.pack(fill="x", padx=20, pady=(0, 20))
        self.control_frame.pack_propagate(False)
        
        # Control buttons container
        self.control_buttons_frame = ctk.CTkFrame(
            self.control_frame,
            fg_color="transparent"
        )
        self.control_buttons_frame.pack(expand=True)
        
        self.play_pause_button = ctk.CTkButton(
            self.control_buttons_frame,
            text="⏸️ PAUSE",
            command=self.toggle_playback,
            fg_color=self.colors["accent"],
            hover_color=self.colors["accent_hover"],
            text_color="#000000",
            font=ctk.CTkFont(size=14, weight="bold"),
            width=120,
            height=40,
            corner_radius=20
        )
        self.play_pause_button.pack(side="left", padx=10)
        
        self.restart_button = ctk.CTkButton(
            self.control_buttons_frame,
            text="🔄 RESTART",
            command=self.restart_video,
            fg_color=self.colors["border"],
            hover_color=self.colors["bg_secondary"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=14, weight="bold"),
            width=120,
            height=40,
            corner_radius=20,
            border_width=2,
            border_color=self.colors["accent"]
        )
        self.restart_button.pack(side="left", padx=10)
        
        self.new_video_button = ctk.CTkButton(
            self.control_buttons_frame,
            text="📁 NEW VIDEO",
            command=self.load_new_video,
            fg_color=self.colors["bg_tertiary"],
            hover_color=self.colors["border"],
            text_color=self.colors["text_primary"],
            font=ctk.CTkFont(size=14, weight="bold"),
            width=140,
            height=40,
            corner_radius=20,
            border_width=2,
            border_color=self.colors["accent"]
        )
        self.new_video_button.pack(side="left", padx=10)
        
    def is_video_file(self, file_path):
        """Check if file can be opened by OpenCV (any format OpenCV supports)"""
        try:
            # Try to open with OpenCV to see if it's a valid video file
            cap = cv2.VideoCapture(file_path)
            if cap.isOpened():
                ret, _ = cap.read()
                cap.release()
                return ret  # Return True if we can read at least one frame
            return False
        except:
            return False
    
    def browse_file(self):
        file_path = filedialog.askopenfilename(
            title="Select Video File - Tennis Ball Tracker",
            filetypes=[
                ("All Video files", "*.*"),
                ("MP4 files", "*.mp4"),
                ("AVI files", "*.avi"),
                ("MOV files", "*.mov"),
                ("MKV files", "*.mkv"),
                ("WMV files", "*.wmv"),
                ("FLV files", "*.flv"),
                ("WEBM files", "*.webm")
            ]
        )
        if file_path:
            if self.is_video_file(file_path):
                self.load_video(file_path)
            else:
                messagebox.showerror("Invalid File", "The selected file cannot be opened as a video.\\n\\nPlease ensure the file is a valid video format that OpenCV can handle.")
    
    def load_video(self, file_path):
        self.video_path = file_path
        
        # Update upload area to show selected file
        filename = os.path.basename(file_path)
        self.upload_icon_label.configure(text="✅")
        self.upload_text_label.configure(text=f"SELECTED: {filename}")
        self.upload_subtext_label.configure(text="Processing will begin shortly...")
        
        # Hide upload frame and show progress
        self.upload_frame.pack_forget()
        self.progress_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Start processing animation
        self.start_processing_animation()
    
    def start_processing_animation(self):
        def animate_progress():
            processing_steps = [
                ("🔍 Analyzing video properties...", 0.2),
                ("🎯 Initializing tennis ball detection...", 0.5),
                ("🧠 Loading AI tracking models...", 0.8),
                ("✅ Processing complete - Ready to track!", 1.0)
            ]
            
            for i, (step, target_progress) in enumerate(processing_steps):
                if not hasattr(self, 'root') or not self.root.winfo_exists():
                    return
                    
                self.progress_status_label.configure(text=step)
                
                # Smooth progress bar animation
                current_progress = self.progress_bar.get()
                steps = 20
                for j in range(steps):
                    if not hasattr(self, 'root') or not self.root.winfo_exists():
                        return
                    progress = current_progress + (target_progress - current_progress) * (j + 1) / steps
                    self.progress_bar.set(progress)
                    self.root.update()
                    time.sleep(0.04)  # Adjusted for 3-4 second total duration
                
                time.sleep(0.8 if i < len(processing_steps) - 1 else 0.5)
            
            # Complete processing
            time.sleep(0.3)
            self.root.after(0, self.initialize_video_playback)
        
        # Run animation in separate thread
        threading.Thread(target=animate_progress, daemon=True).start()
    
    def initialize_video_playback(self):
        try:
            self.video_cap = cv2.VideoCapture(self.video_path)
            if not self.video_cap.isOpened():
                messagebox.showerror("Video Error", "Could not open video file\\n\\nPlease ensure the file is not corrupted and try again.")
                self.reset_to_upload()
                return
            
            # Initialize Kalman filter
            self.kf = KalmanFilter()
            
            # Hide progress and show video
            self.progress_frame.pack_forget()
            self.video_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
            
            # Start video playback
            self.is_playing = True
            self.play_video()
            
        except Exception as e:
            messagebox.showerror("Initialization Error", f"Failed to initialize video playback:\\n\\n{str(e)}")
            self.reset_to_upload()
    
    def process_frame(self, frame):
        """Process frame with tennis ball tracking and enhanced visualization with orange/green contrast"""
        # Get window dimensions for responsive sizing
        window_width = self.video_label.winfo_width() if self.video_label.winfo_width() > 1 else 800
        window_height = self.video_label.winfo_height() if self.video_label.winfo_height() > 1 else 600
        
        # Resize frame to fit the GUI window while maintaining aspect ratio
        frame_height, frame_width = frame.shape[:2]
        aspect_ratio = frame_width / frame_height
        
        if window_width / aspect_ratio <= window_height:
            new_width = window_width
            new_height = int(window_width / aspect_ratio)
        else:
            new_height = window_height
            new_width = int(window_height * aspect_ratio)
            
        frame = cv2.resize(frame, (new_width, new_height))
        
        # Tennis ball detection
        blurred = cv2.GaussianBlur(frame, (11, 11), 0)
        hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)
        mask = cv2.inRange(hsv, self.greenLower, self.greenUpper)
        mask = cv2.erode(mask, None, iterations=2)
        mask = cv2.dilate(mask, None, iterations=2)
        
        contours, _ = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Kalman filter prediction
        predicted_coords = self.kf.predict()
        
        # Enhanced visualization with orange (detected) and green (predicted) contrast
        detection_found = False
        if len(contours) > 0:
            c = max(contours, key=cv2.contourArea)
            ((x, y), radius) = cv2.minEnclosingCircle(c)
            
            if radius > 10:
                detection_found = True
                # Update Kalman filter with detection
                measurement = np.array([[np.float32(x)], [np.float32(y)]])
                self.kf.update(measurement)
                
                # Draw detection circle with ORANGE accent (BGR format: B=17, G=163, R=252 for #fca311)
                cv2.circle(frame, (int(x), int(y)), int(radius), (17, 163, 252), 3)  # Orange detection
                cv2.circle(frame, (int(x), int(y)), int(radius + 5), (50, 180, 255), 1)  # Outer glow
                
                # Add detection label with orange color
                cv2.putText(frame, "DETECTED", (int(x) - 40, int(y) - int(radius) - 20), 
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (17, 163, 252), 2)
        
        # Draw Kalman filter prediction with GREEN (BGR format: B=83, G=200, R=0 for #00C853)
        pred_x, pred_y = int(predicted_coords[0]), int(predicted_coords[1])
        cv2.circle(frame, (pred_x, pred_y), 8, (83, 200, 0), 2)  # Green prediction
        cv2.circle(frame, (pred_x, pred_y), 12, (100, 220, 0), 1)  # Prediction outer ring
        
        # Add prediction label with green color
        cv2.putText(frame, "PREDICTED", (pred_x - 45, pred_y - 25), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (83, 200, 0), 2)
        
        # Add status overlay with orange/green theme
        status_text = "TRACKING ACTIVE" if detection_found else "SEARCHING..."
        status_color = (83, 200, 0) if detection_found else (17, 163, 252)
        cv2.putText(frame, status_text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, status_color, 2)
        
        # Add coordinate display
        cv2.putText(frame, f"Pred: ({pred_x}, {pred_y})", (10, frame.shape[0] - 40), 
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (83, 200, 0), 2)
        
        if detection_found:
            cv2.putText(frame, f"Det: ({int(x)}, {int(y)})", (10, frame.shape[0] - 15), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (17, 163, 252), 2)
        
        return frame
    
    def play_video(self):
        if not self.is_playing or not self.video_cap:
            return
        
        ret, frame = self.video_cap.read()
        if not ret:
            # Restart video for endless loop
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            ret, frame = self.video_cap.read()
            # Reset Kalman filter for new loop
            if self.kf:
                self.kf = KalmanFilter()
        
        if ret:
            # Process frame with tennis ball tracking
            processed_frame = self.process_frame(frame)
            
            # Convert to RGB and then to PhotoImage
            frame_rgb = cv2.cvtColor(processed_frame, cv2.COLOR_BGR2RGB)
            frame_pil = Image.fromarray(frame_rgb)
            frame_tk = ImageTk.PhotoImage(frame_pil)
            
            # Update video label
            self.video_label.configure(image=frame_tk)
            self.video_label.image = frame_tk  # Keep a reference
        
        # Schedule next frame (30 FPS)
        self.root.after(33, self.play_video)
    
    def toggle_playback(self):
        if not self.video_cap:
            return
            
        self.is_playing = not self.is_playing
        if self.is_playing:
            self.play_pause_button.configure(text="⏸️ PAUSE")
            self.tracking_status_label.configure(text="● ACTIVE", text_color=self.colors["accent_secondary"])
            self.play_video()
        else:
            self.play_pause_button.configure(text="▶️ PLAY")
            self.tracking_status_label.configure(text="● PAUSED", text_color=self.colors["warning"])
    
    def restart_video(self):
        if self.video_cap:
            self.video_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
            if self.kf:
                self.kf = KalmanFilter()  # Reset Kalman filter
            self.tracking_status_label.configure(text="● RESTARTED", text_color=self.colors["accent"])
            # Reset status after a moment
            self.root.after(1000, lambda: self.tracking_status_label.configure(text="● ACTIVE", text_color=self.colors["accent_secondary"]))
    
    def load_new_video(self):
        """Load a new video file"""
        self.reset_to_upload()
    
    def reset_to_upload(self):
        """Reset the interface to the upload state"""
        # Stop current video
        self.is_playing = False
        if self.video_cap:
            self.video_cap.release()
            self.video_cap = None
        
        # Hide video frame
        self.video_frame.pack_forget()
        self.progress_frame.pack_forget()
        
        # Reset upload frame
        self.upload_icon_label.configure(text="📁")
        self.upload_text_label.configure(text="DRAG & DROP YOUR VIDEO FILE HERE")
        self.upload_subtext_label.configure(text="Supports any format that OpenCV can handle (MP4, AVI, MOV, MKV, WMV, etc.)")
        
        # Show upload frame
        self.upload_frame.pack(fill="x", padx=30, pady=(0, 20))
        
        # Reset variables
        self.video_path = None
        self.kf = None
        self.processing_complete = False
    
    def run(self):
        try:
            # Center the window on screen
            self.root.update_idletasks()
            width = self.root.winfo_width()
            height = self.root.winfo_height()
            x = (self.root.winfo_screenwidth() // 2) - (width // 2)
            y = (self.root.winfo_screenheight() // 2) - (height // 2)
            self.root.geometry(f"{width}x{height}+{x}+{y}")
            
            self.root.mainloop()
        except KeyboardInterrupt:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        self.is_playing = False
        if self.video_cap:
            self.video_cap.release()
        if hasattr(self, 'root'):
            self.root.destroy()

if __name__ == "__main__":
    try:
        app = TennisBallTrackerGUI()
        app.run()
    except Exception as e:
        print(f"Error starting application: {e}")
        input("Press Enter to exit...")