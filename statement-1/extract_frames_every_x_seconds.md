# Extracting Frames from a Video at Regular Intervals

To extract one frame every *X* seconds, you need to understand the video's FPS (frames per second).

Since videos are stored as frames internally, not seconds, this conversion is essential.

## Example:

**Video FPS = 30**

This means:
- 1 second = 30 frames

If the goal is to extract 1 frame every 2 seconds, you must skip:
- `2 × 30 = 60` frames

## Step 1 — Ask User for Seconds Input
Add this after the YouTube URL input:
```python
interval = int(input("Extract frame every X seconds (1-10): "))
```

## Step 2 — Get Video FPS
OpenCV allows you to read the FPS like this:
```python
fps = cap.get(cv2.CAP_PROP_FPS)
```
**Example output:**
fps = 30

## Step 3 — Convert Seconds to Frame Interval
Calculate the number of frames to skip based on the interval:
```python
frame_interval = int(fps * interval)
```
**Example:**
fps = 30, interval = 2,
```python
frame_interval = 60
```
This means:
- Save a frame every **60 frames**
during processing.

## Step 4 — Save Only Selected Frames
Modify your loop so it only saves frames at that specified interval.