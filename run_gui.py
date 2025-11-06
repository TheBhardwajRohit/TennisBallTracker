"""
Tennis Ball Tracker GUI Launcher
================================

This script launches the Tennis Ball Tracker GUI application.
Make sure you have the required dependencies installed:
- customtkinter
- opencv-python
- pillow
- numpy

Usage: python run_gui.py
"""

import sys
import os

def check_dependencies():
    """Check if required packages are installed"""
    required_packages = [
        'customtkinter',
        'cv2',
        'PIL',
        'numpy'
    ]
    
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package} - OK")
        except ImportError:
            missing_packages.append(package)
            print(f"❌ {package} - NOT FOUND")
    
    if missing_packages:
        print(f"\\n⚠️  Missing packages: {', '.join(missing_packages)}")
        print("\\nTo install missing packages, run:")
        print("pip install customtkinter opencv-python pillow numpy")
        return False
    
    print("\\n🎉 All dependencies found!")
    return True

def main():
    print("🎾 Tennis Ball Tracker GUI")
    print("=" * 30)
    print("🎨 Modern Teal Accent Theme")
    print("🔍 Supports any OpenCV-compatible video format")
    print("")
    
    # Check dependencies
    if not check_dependencies():
        input("\\nPress Enter to exit...")
        sys.exit(1)
    
    print("\\n🚀 Starting application...")
    
    try:
        # Import and run the GUI
        from tennis_ball_tracker_gui_simple import TennisBallTrackerGUI
        
        app = TennisBallTrackerGUI()
        app.run()
        
    except Exception as e:
        print(f"\\n❌ Error starting application: {e}")
        print("\\nTroubleshooting tips:")
        print("1. Ensure all dependencies are properly installed")
        print("2. Check that your video file is in a format OpenCV can handle")
        print("3. Make sure you have sufficient permissions")
        
        input("\\nPress Enter to exit...")
        sys.exit(1)

if __name__ == "__main__":
    main()