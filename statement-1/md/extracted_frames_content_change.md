### **Core Idea**

For every frame:

```
previous_frame -> compare -> current_frame
```


If the difference is large -> slide changed -> save frame



#### Step-1 : Mease Frame Difference

OpenCV can compute the absolute difference between two frames :

```
diff = cv2.absdiff(prev_frame, frame)
```

This produces an image representing how different the frames are.


Then we measure how big the difference is:

```
score = diff.mean()
```

Large score -> Big change


#### Step-2 : Save Frame When Difference is Large

If the score crosses a threshold:

```
if score > threshold:
```

we save the frame.



#### Important Parameters : **Threshold control**


```
threshold = 10 -> very sensitive
threshold = 25 -> good for slides
threshold = 50 -> defected only large changes
```


For PPT videos:

```
20-35 usually works well
```