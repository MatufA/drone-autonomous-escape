# drone-autonomous-escape
Our project focuses on a "DJI Tello" drone, making it autonomously evade obsticles.
We focused on evading trees, by processing the video from the drone at real time, and built an algorithm which will make it avoid the trees.

### why havn't we used object detection methods like yolo/haar cascades/SSD?
At first, we tried to find (unsuccessfully) a trained weights for haar cascades.
Then, we tried to train a haar cascade for detecting trees, but because *need to complete*.

SSD is not doing really well in real time.

Yolo could've been fine, but also wasnt fast enough. We had limited resources and couldn't afford new laptop just for that project.

### HSV - range of brown detection.





# Credits
[ofikodar](https://github.com/ofikodar) for using his repository [drone-auto-landing](https://github.com/ofikodar/drone-auto-landing)
