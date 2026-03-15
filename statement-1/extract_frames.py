import yt_dlp
import cv2
import os


# YouTube video URL
url = input("Enter the youtube video link: ")

# This will save the downloaded video with this name as "video.mp4"
output_video = "video.mp4"

# Dictionary of configurations
ydl_opts = {
    'outtmpl': output_video
}


with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Video downloaded!")


# Create folder for frames
output_folder = "frames"
os.makedirs(output_folder, exist_ok=True)


# Read video
cap = cv2.VideoCapture(output_video)

frame_count = 0

while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
    cv2.imwrite(frame_filename, frame)

    frame_count += 1


cap.release()

print("Total frames extracted: ", frame_count)