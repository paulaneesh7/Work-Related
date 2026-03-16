### Things I learnt about :

- pytube -> to download youtube videos
- opencv-pythong -> processess video and extract frames




```
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
```

means :

```
Here we take the video link as user_input and then save it with the name of video.mp4 and we define a dictionary of configuration and then with yt_dlp we download the video and then print video downloaded and then create a folder named "frames" to store the extracted frames from the video and then we read the video with cv2's VideoCapture where we directly provide the downloaded video and then there's this variable with keeps a count of the no. of frames
```


- What does `cv2.VideoCapture()` do?
  ```
  cap = cv2.VideoCapture(output_video)
  ```

  This tells OpenCV that "Open this video file so that I can read its frames"

  video.mp4 -> OpenCV opens the file -> cap object can now read frames


- What is `while True` doing?
  ```
  while True:
  ```

  It keeps running the block until we manually stop it or the inside break condition executes

  Read frame -> Process frame -> Read next frame -> Process frame -> Repeat (until the video ends)


- What does this line do?
  ```
  ret, frame = cap.read()
  ```

  **This is the most important OpenCV line**

  `cap.read()` does 2 things:
  - Reads the next frame from the video
  - Returns two values :
    - ret (Boolean value) : 
      - True: frame was successfully read
      - False: no more frames (video ended)
    - frame (actual image of the frame)
      - Internally it is NumPy array (hight x width x color_channels)


- Why this condition :
  ```
  if not ret:
    break
  ```

  Meaning: If frame reading failed -> stop the loop (this happens when video reached its last frame)

- What does this line do:
  ```
  frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
  ```

  **This creates a file path**

  Example :
  ```
  frames/frame_0.jpg
  frames/frame_1.jpg
  frames/frame_2.jpg
  ```
  
  `os.path.join()` is used because it's cross-platform safe.



- What does `cv2.imwrite() does :
  ```
  cv2.imwrite(frame_filename, frame)
  ```

  **This saves the frame as an image file**

  frame -> image

  output :
  ```
  frames/frame_0.jpg
  frames/frame_1.jpg
  frames/frame_2.jpg
  ```

- What does `cap.release()` do:
  This closes the video file

- So we :
  - Open file
  - Read file
  - Close file





```
while True:
    ret, frame = cap.read()

    if not ret:
        break

    frame_filename = os.path.join(output_folder, f"frame_{frame_count}.jpg")
    cv2.imwrite(frame_filename, frame)

    frame_count += 1


cap.release()

print("Total frames extracted: ", frame_count)
```


In this above code we read the next frame from the video which returns 2 things `ret` and `frame` where `ret` represents Boolean value which tells whether the frame was read successfully or not and `frame` is the actual video frame

If `ret` is not present anymore then it means we have reached the video end (as frames aren't present anymore) then we break out of the loop

We also save the frame inside the provided output folder with the naming convention `frame_{frame_count}.jpg` eg: frame_1.jpg, frame_2.jpg etc...

Then at the end we close the video with `cap.release()`