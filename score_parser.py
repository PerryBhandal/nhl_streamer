import cv2
import pytesseract

# Load the image and define the ROI
img = cv2.imread('path_to_image.png')
x, y, w, h = 100, 100, 200, 50
roi = img[y:y+h, x:x+w]

# Convert the ROI to grayscale and apply thresholding
gray = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)
thresh = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

# Use Tesseract OCR to extract the text
text = pytesseract.image_to_string(thresh)

print(text)
