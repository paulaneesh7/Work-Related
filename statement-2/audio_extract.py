import moviepy

def ExtractAudio(video_path):
    video = moviepy.VideoFileClip(video_path)
    audio = video.audio
    duration = audio.duration
    fps = audio.fps
    audio.write_audiofile("extracted_audio.mp3", fps=fps)

    audio.close()
    video.close()

    return duration, fps


if __name__ == "__main__":
    video_path = "video.mp4"
    duration, fps = ExtractAudio(video_path)
    print(f"Audio extracted with duration: {duration} seconds and fps: {fps}")



    