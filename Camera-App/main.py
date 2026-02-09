# Install the required libraries
# pip install pyqt5 opencv-contrib-python

# System and file handling
import os
import sys
from datetime import datetime

# PyQt5 interface components
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QPushButton, QGridLayout, QMessageBox, QSpacerItem
from PyQt5.QtGui import QPixmap, QImage, QIcon
from PyQt5.QtCore import QTimer, QSize
from PyQt5.QtWidgets import QSizePolicy

# OpenCV for video capture and processing
import cv2

BASE_DIR = os.path.dirname(__file__)
camera_icon_path = os.path.join(BASE_DIR, "assets", "camera.png")
video_camera_icon_path = os.path.join(BASE_DIR, "assets", "video-camera.png")
pause_icon_path = os.path.join(BASE_DIR, "assets", "pause.png")
stop_icon_path = os.path.join(BASE_DIR, "assets", "stop.png")
CAPTURES_DIR = os.path.join(BASE_DIR, "captures")

# Create captures directory if it doesn't exist
if not os.path.exists(CAPTURES_DIR):
    os.makedirs(CAPTURES_DIR)

if not os.path.exists(camera_icon_path):
    print("Icon not found:", camera_icon_path)

def get_timestamp():
    """Generate a timestamp string for filenames"""
    return datetime.now().strftime("%Y%m%d_%H%M%S")

class Window(QWidget):
    def __init__(self):
        super().__init__()
        
        # variables for app window
        self.window_width = 800
        self.window_height = 540

        # image variables
        self.image_width = 640
        self.image_height = 480

        # icons
        self.camera_icon = QIcon(camera_icon_path)
        self.video_camera_icon = QIcon(video_camera_icon_path)
        self.pause_icon = QIcon(pause_icon_path)
        self.stop_icon = QIcon(stop_icon_path)

        # video recording variables
        self.is_recording = False
        self.is_paused = False
        self.video_filepath = None

        # set up the window
        self.setWindowTitle('Camera App')
        self.setGeometry(100, 100, self.window_width, self.window_height)
        self.setFixedSize(self.window_width, self.window_height)

        # set up timer
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)

        self.ui()
    
    def ui(self):
        # layout
        grid = QGridLayout()
        grid.setSpacing(12)
        grid.setContentsMargins(0, 0, 0, 0)  # Maximize available space
        self.setLayout(grid)

        # camera feed display
        self.label = QLabel(self)
        self.label.setFixedSize(self.image_width, self.image_height)
        self.label.setStyleSheet("background-color: #000; border: none;")

        # capture button
        self.capture_button = QPushButton(self)
        self.capture_button.setIcon(self.camera_icon)
        self.capture_button.setIconSize(QSize(40, 40))
        self.capture_button.setFixedSize(70, 70)
        self.capture_button.setToolTip("Capture Photo")
        self.capture_button.clicked.connect(self.save_image)
        self.capture_button.setStyleSheet("border-radius: 10px;")

        # record button (start/stop)
        self.record_button = QPushButton(self)
        self.record_button.setIcon(self.video_camera_icon)
        self.record_button.setIconSize(QSize(40, 40))
        self.record_button.setFixedSize(70, 70)
        self.record_button.setToolTip("Start Recording")
        self.record_button.clicked.connect(self.toggle_recording)
        self.record_button.setStyleSheet("border-radius: 10px;")

        # pause button (pause/resume) - initially hidden
        self.pause_button = QPushButton(self)
        self.pause_button.setIcon(self.pause_icon)
        self.pause_button.setIconSize(QSize(40, 40))
        self.pause_button.setFixedSize(70, 70)
        self.pause_button.setToolTip("Pause Recording")
        self.pause_button.clicked.connect(self.toggle_pause)
        self.pause_button.setStyleSheet("border-radius: 10px;")
        self.pause_button.setVisible(False)  # Hidden until recording starts

        if not self.timer.isActive():
            self.capture = cv2.VideoCapture(0)  # Open the default camera (0)
            self.timer.start(20)
        
        # add widgets to the grid layout - buttons on the left, camera feed on the right
        grid.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 0, 0)  # Stretch above
        grid.addWidget(self.capture_button, 1, 0)
        grid.addWidget(self.record_button, 2, 0)
        grid.addWidget(self.pause_button, 3, 0)
        grid.addItem(QSpacerItem(0, 0, QSizePolicy.Minimum, QSizePolicy.Expanding), 4, 0)  # Stretch below
        grid.addWidget(self.label, 0, 1, 5, 1)

        # start the camera
        self.show()

    def save_image(self):
        try:
            if not hasattr(self, 'frame') or self.frame is None:
                QMessageBox.warning(self, "Error", "No frame captured yet!")
                return
            
            # Generate filename with timestamp
            timestamp = get_timestamp()
            filename = f"capture_{timestamp}.png"
            filepath = os.path.join(CAPTURES_DIR, filename)
            
            # Save the frame
            success = cv2.imwrite(filepath, self.frame)
            
            if success:
                QMessageBox.information(self, "Success", f"Image saved:\n{filename}")
                print(f"Image saved: {filepath}")
            else:
                QMessageBox.warning(self, "Error", "Failed to save image!")
        except Exception as e:
            QMessageBox.critical(self, "Error", f"An error occurred:\n{str(e)}")
            print(f"Error saving image: {e}")
    
    def toggle_recording(self):
        """Start or stop video recording"""
        if not self.is_recording:
            # Start recording
            timestamp = get_timestamp()
            filename = f"video_{timestamp}.avi"
            self.video_filepath = os.path.join(CAPTURES_DIR, filename)
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(
                self.video_filepath, fourcc, 20.0, 
                (self.image_width, self.image_height)
            )
            
            # Update button states
            self.record_button.setIcon(self.stop_icon)
            self.record_button.setToolTip("Stop Recording")
            self.pause_button.setVisible(True)  # Show pause button
            self.is_recording = True
            self.is_paused = False
            print(f"Recording started: {self.video_filepath}")
        else:
            # Stop recording
            self.video_writer.release()
            self.record_button.setIcon(self.video_camera_icon)
            self.record_button.setToolTip("Start Recording")
            self.pause_button.setVisible(False)  # Hide pause button
            self.pause_button.setIcon(self.pause_icon)
            self.pause_button.setToolTip("Pause Recording")
            self.is_recording = False
            self.is_paused = False
            
            QMessageBox.information(
                self, "Success", 
                f"Video saved:\n{os.path.basename(self.video_filepath)}"
            )
            print(f"Video saved: {self.video_filepath}")

    def toggle_pause(self):
        """Pause or resume video recording"""
        if not self.is_recording:
            return
        
        if not self.is_paused:
            # Pause recording
            self.is_paused = True
            self.pause_button.setToolTip("Resume Recording")
            print("Recording paused")
        else:
            # Resume recording
            self.is_paused = False
            self.pause_button.setToolTip("Pause Recording")
            print("Recording resumed")

    def update_frame(self):
        _, self.frame = self.capture.read()  # Read a frame from the camera
        frame = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # Convert BGR to RGB
        height, width, channel = frame.shape
        step = channel * width
        qImg = QImage(frame.data, width, height, step, QImage.Format_RGB888)
        self.label.setPixmap(QPixmap.fromImage(qImg))
        
        # Write frame to video if recording and not paused
        if self.is_recording and not self.is_paused and hasattr(self, 'video_writer'):
            self.video_writer.write(self.frame)

    def closeEvent(self, event):
        """Clean up resources when closing the window"""
        if self.is_recording:
            self.video_writer.release()
        if hasattr(self, 'capture'):
            self.capture.release()
        cv2.destroyAllWindows()
        event.accept()


if __name__ == '__main__':
    # Create the application and the main window
    app = QApplication(sys.argv)
    window = Window()
    sys.exit(app.exec_())