import cv2
import pytesseract

# Set the path to the Tesseract executable file
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load the video
cap = cv2.VideoCapture("test_video.mp4")

# Get the first frame and display it
ret, img = cap.read()
cv2.imshow("Frame", img)

# Define the callback function for mouse events
def select_roi(event, x, y, flags, params):
    global roi, roi_gray
    if event == cv2.EVENT_LBUTTONDOWN:
        # Start selecting the ROI
        roi = (x, y)
    elif event == cv2.EVENT_LBUTTONUP:
        # Finish selecting the ROI
        w = x - roi[0]
        h = y - roi[1]
        roi = (roi[0], roi[1], w, h)
        roi_gray = gray[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
        cv2.rectangle(img, roi[:2], (roi[0]+roi[2], roi[1]+roi[3]), (0, 255, 0), 2)
        cv2.imshow("Frame", img)

# Convert the first frame to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Define the ROI using mouse events
roi = None
roi_gray = None
cv2.namedWindow("Frame")
cv2.setMouseCallback("Frame", select_roi)
cv2.waitKey(0)

# Process each frame of the video
while True:
    # Read the next frame
    ret, img = cap.read()
    if not ret:
        break

    # Extract the text within the ROI using Pytesseract
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    roi_gray = gray[roi[1]:roi[1]+roi[3], roi[0]:roi[0]+roi[2]]
    text = pytesseract.image_to_string(roi_gray, config='--psm 10 --oem 3 -c tessedit_char_whitelist=0123456789')

    # Print the current time and extracted text to the console
    current_time = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000
    print("Current time:", current_time)
    print("Text within bounding box:", text)

    # Display the frame with the bounding box
    cv2.rectangle(img, roi[:2], (roi[0]+roi[2], roi[1]+roi[3]), (0, 255, 0), 2)
    cv2.imshow("Frame", img)

    # Check for key presses and break if 'q' is pressed
    if cv2.waitKey(1) == ord('q'):
        break

# Cleanup
cap.release()
cv2.destroyAllWindows()
