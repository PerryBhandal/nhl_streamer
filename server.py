import subprocess
import datetime
import os

# Replace this with the YouTube live stream URL you want to download
youtube_url = "https://www.youtube.com/watch?v=your_video_id"

# Generate a timestamp for the output file name
timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

# Set the initial output file name
output_filename = f"game_stream_{timestamp}_1.mkv"

# Set the maximum file size in bytes (500 megabytes)
max_file_size = 500 * 1024 * 1024

# Set the initial file size to 0
file_size = 0

# Build the ffmpeg command
ffmpeg_command = f"ffmpeg -i '{youtube_url}' -c copy '{output_filename}'"

# Start the ffmpeg process
process = subprocess.Popen(ffmpeg_command, shell=True)

# Wait for the process to finish
while process.poll() is None:
    # Check the size of the output file
    file_size = os.path.getsize(output_filename)
    
    # If the file size exceeds the maximum file size
    if file_size > max_file_size:
        # Increment the file name
        parts = output_filename.split("_")
        count = int(parts[-1].split(".")[0])
        count += 1
        parts[-1] = f"{count}.mkv"
        output_filename = "_".join(parts)
        
        # Start a new ffmpeg process with the updated file name
        ffmpeg_command = f"ffmpeg -i '{youtube_url}' -c copy '{output_filename}'"
        process.kill()  # Kill the old ffmpeg process
        process = subprocess.Popen(ffmpeg_command, shell=True)
    
    # Wait for 10 seconds before checking the file size again
    time.sleep(10)
    
# Cleanup the process
process.kill()
