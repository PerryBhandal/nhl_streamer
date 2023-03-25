import cv2
import pytesseract

# Load the image
img = cv2.imread("test_scoreboard.png")

# Display the image and let the user select the ROI
roi = cv2.selectROI(img)

# Extract the text within the ROI using Pytesseract
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
x, y, w, h = roi
roi_gray = gray[y:y+h, x:x+w]
text = pytesseract.image_to_string(roi_gray)

# Draw a rectangle around the ROI and display the result
cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
cv2.imshow("Image with ROI", img)
cv2.waitKey(0)
cv2.destroyAllWindows()

# Print the extracted text
print("The extracted text is " + text)
print(text)
