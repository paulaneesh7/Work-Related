import yt_dlp
import cv2
import os
from moviepy import VideoFileClip
import whisper
from transformers import pipeline


####################################
# 1. Download YouTube video
####################################

url = input("Enter YouTube URL: ")

video_file = "video.mp4"

ydl_opts = {
    "outtmpl": video_file
}

with yt_dlp.YoutubeDL(ydl_opts) as ydl:
    ydl.download([url])

print("Video downloaded!")


####################################
# 2. Extract Slides (scene changes)
####################################

slides_folder = "slides"
os.makedirs(slides_folder, exist_ok=True)

cap = cv2.VideoCapture(video_file)

ret, prev_frame = cap.read()

slide_count = 0
threshold = 25

while True:

    ret, frame = cap.read()
    if not ret:
        break

    diff = cv2.absdiff(prev_frame, frame)
    score = diff.mean()

    if score > threshold:

        filename = os.path.join(slides_folder, f"slide_{slide_count}.jpg")
        cv2.imwrite(filename, frame)

        slide_count += 1

    prev_frame = frame

cap.release()

print("Slides extracted:", slide_count)


####################################
# 3. Extract Audio
####################################

video = VideoFileClip(video_file)

audio_file = "audio.wav"

video.audio.write_audiofile(audio_file)

print("Audio extracted!")


####################################
# 4. Speech to Text
####################################

model = whisper.load_model("base")

result = model.transcribe(audio_file)

transcript = result["text"]

with open("transcript.txt", "w") as f:
    f.write(transcript)

print("Transcript generated!")


####################################
# 5. Generate Summary
####################################

summarizer = pipeline("summarization")

summary = summarizer(transcript, max_length=200, min_length=50)

notes = summary[0]["summary_text"]

with open("notes.txt", "w") as f:
    f.write(notes)

print("Summary generated!")