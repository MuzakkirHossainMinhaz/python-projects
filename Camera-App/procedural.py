# Install the required libraries
# pip install opencv-contrib-python

import cv2

capture = cv2.VideoCapture(0) # Open the default camera (0)

while True:
    _, frame = capture.read() # Read a frame from the camera

    # Display the frame in a window named 'Camera'
    cv2.imshow('Camera', frame)

    # Wait for 1 millisecond and check if the 'q' key is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break # Exit the loop if 'q' is pressed

capture.release() # Release the camera
cv2.destroyAllWindows() # Close all OpenCV windows