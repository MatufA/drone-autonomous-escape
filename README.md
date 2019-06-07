# drone-autonomous-escape
Our project focuses on a "DJI Tello" drone, making it autonomously evade obsticles.
We focused on evading trees, by processing the video from the drone at real time, and built an algorithm which will make it avoid the trees.

### why havn't we used object detection methods like yolo/haar cascades/SSD?
At first, we tried to find (unsuccessfully) a trained weights for haar cascades.
So, we tried to train a haar cascade for detecting trees, but it's isn't fit to our goal.

Then, we tried to use SSD, but SSD isn't doing really well in real time (for 30 FPS minimum, with our hardware).

We also tried to use YoloV3, Yolo  been great for detecting an object in real time. 
We decide to train our costume object but we had a lot of problem with YoloV3, C++ and Python.
So, we look for a weight and found a weight for 9000+ object (with a lot of tree type, perfect for our mission) 
but it also wasn't fast enough. (for 30 FPS minimum, with our hardware)


Finally, after consulting some people from the KGC lab, we tried to use some image processing manipulations in order to see if we can decide whats a tree by detecting spesific range & amount of brown pixels.
First we found a code which detects green contours, so we thought we might lead the drone by the detected green. Problem is that it also detected some low trees leaves. Then we manipulated the code a bit and decided to detect a range of brown. At the beginning we detected too many because of noise, so we tried to minimize the noise with some more OpenCV manipulations but it wasn't good enough.
After testing and with the help of Dr. Ben-Moshe we found out that when the drone is about to crash into a tree the tree is 
detected from bottom up.
We started with a simple model which described below.

### HSV - range of brown detection.
HSV is a Hue Saturation Value(Brightness). HSV is defined in a way that is similar to how humans perceive color. 
It's based on three values: hue, saturation, and value. This color space describes colors (hue or tint) in terms of 
their shade (saturation or amount of gray) and their brightness value. Some color pickers use the acronym HSB, which 
substitutes the term brightness for value, but HSV and HSB refer to the same color model. (a short explanation from 
[lifewire](https://www.lifewire.com/what-is-hsv-in-design-1078068)).  
After a lot of testing we found out that the best result for us (in outdoor gardens):  
* H range is 10 - 20.
* S range is 20 - 150.
* V(B) range is 20 - 100.

Our [brown detector](detect_model/brown_detection.py) is an implementation of brown detector with OpenCV.




# Credits
[ofikodar](https://github.com/ofikodar) for using his repository [drone-auto-landing](https://github.com/ofikodar/drone-auto-landing)
