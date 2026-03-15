import yt_dlp
import cv2
import os


# Youtube video url
url = input("Enter the youtube video link: ")


# Ask user for frame extraction interval
interval = int(input("Extract frame every x seconds (1-10): "))


# Output video name
output_video = "video.mp4"


# Download configurations
ydl_opts = {
    'outtmpl': output_video
}


# Download video
with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])


print("Video downloaded")



# Create frames folder
output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)



# Read video
cap = cv2.VideoCapture(output_video)

# Get FPS
fps = cap.get(cv2.CAP_PROP_FPS)


# Convert seconds -> frame interval
frame_interval = int(fps * interval)

frame_count = 0
saved_frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    # Save frame only at the interval
    if frame_count % frame_interval == 0:
        frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
        cv2.imwrite(frame_filename, frame)
        saved_frame_count += 1
    
    frame_count += 1


cap.release()

print("Total frames extracted: ", saved_frame_count)
