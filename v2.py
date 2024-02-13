import cv2
import pytesseract
import subprocess
import numpy as np
import time

import pytesseract
pytesseract.pytesseract.tesseract_cmd = '/usr/bin/tesseract' 

# Function to start the stream and return a pipe
def start_stream(youtube_url):
    # Use Streamlink to get the best quality stream URL
    stream_url = subprocess.run(['streamlink', youtube_url, 'best', '--stream-url'], stdout=subprocess.PIPE).stdout.decode('utf-8').strip()
    # Open a pipe from the stream URL to capture video frames
    video_pipe = subprocess.Popen(['ffmpeg', '-i', stream_url, '-loglevel', 'quiet', '-f', 'image2pipe', '-pix_fmt', 'bgr24', '-vcodec', 'rawvideo', '-'], stdout=subprocess.PIPE, bufsize=10**8)
    return video_pipe

def extract_text_from_frame(frame, x, y, width, height):
    # Crop the region from the frame
    region = frame[y:y+height, x:x+width]

    # Resize the region
    region = cv2.resize(region, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)

    # Convert the region to grayscale
    gray = cv2.cvtColor(region, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Apply thresholding
    _, thresholded = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

    # Use Tesseract to do OCR on the region
    text = pytesseract.image_to_string(thresholded, config='--psm 13 -c tessedit_char_whitelist=0123456789')

    return text

def main(youtube_url, regions):
    video_pipe = start_stream(youtube_url)
    width, height = 1920, 1080  # Assume 1080p for this example; adjust as needed

    frame_counter = 0  # Initialize a counter for the frames

    while True:
        # Read a frame from the video pipe
        raw_image = video_pipe.stdout.read(width * height * 3)
        if not raw_image:
            break  # Break if no more frames

        frame_counter += 1  # Increment the counter

        if frame_counter == 30:  # If this is the 30th frame
            # Convert the frame to a format OpenCV can use
            frame = np.frombuffer(raw_image, np.uint8).reshape((height, width, 3))

            # Create a writable copy of the frame
            frame_copy = frame.copy()

            # Draw a debug box around the first region
            x, y, w, h = regions[0]
            cv2.rectangle(frame_copy, (x, y), (x+w, y+h), (0, 255, 0), 2)  # Green box

            for i, (x, y, w, h) in enumerate(regions):
                text = extract_text_from_frame(frame, x, y, w, h)
                print(f"Text from region {i+1}: {text}")

            cv2.imshow('Frame', frame_copy)
            if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to quit
                break

            frame_counter = 0  # Reset the counter

        # Skip to the next frame in the pipe
        video_pipe.stdout.flush()

    cv2.destroyAllWindows()

if __name__ == "__main__":
    youtube_url = 'https://www.youtube.com/watch?v=Qf1hciH75cw'
    regions = [
        (725, 1019, 100, 61),  # x, y, width, height for the first region
        (1079, 1020, 129, 62),  # x, y, width, height for the second region
    ]
    main(youtube_url, regions)

