import cv2
import pytesseract

# Set the path to the Tesseract executable file
pytesseract.pytesseract.tesseract_cmd = "/usr/bin/tesseract"

# Load the image
img = cv2.imread("test_scoreboard.png")

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
        text = pytesseract.image_to_string(roi_gray, config='--psm 6')
        print(text)
        cv2.rectangle(img, roi[:2], (roi[0]+roi[2], roi[1]+roi[3]), (0, 255, 0), 2)
        cv2.imshow("Image", img)

# Set up the mouse event callback
cv2.namedWindow("Image")
cv2.setMouseCallback("Image", select_roi)

# Convert the image to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Display the image
cv2.imshow("Image", img)

# Wait for a key press
cv2.waitKey(0)

# Cleanup
cv2.destroyAllWindows()
