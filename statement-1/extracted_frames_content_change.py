import yt_dlp
import cv2
import os


# url = input("Enter the youtube video link: ")

# output_video = "video.mp4"

# ydl_opts = {
#     'outtmpl': output_video
# }

# with yt_dlp.YoutubeDL(ydl_opts) as ydl:
#     ydl.download([url])

# print("Video downloaded!")

video_path = "video_slide.mp4"

output_folder = "slides"
os.makedirs(output_folder, exist_ok=True)

cap = cv2.VideoCapture(video_path)

ret, prev_frame = cap.read()

frame_count = 0
saved_count = 0

threshold = 28   # controls sensitivity

while True:

    ret, frame = cap.read()

    if not ret:
        break

    diff = cv2.absdiff(prev_frame, frame)

    score = diff.mean()

    if score > threshold:
        filename = os.path.join(output_folder, f"slide_{saved_count}.jpg")
        cv2.imwrite(filename, frame)
        saved_count += 1

    prev_frame = frame
    frame_count += 1


cap.release()

print("Slides detected:", saved_count)