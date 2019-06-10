# drone-autonomous-escape
Our project focuses on a "DJI Tello" drone, making it autonomously evade obsticles.
We focused on evading trees, by processing the video from the drone at real time, and built an algorithm which will make it avoid the trees.

![alt text](https://forum44.djicdn.com/data/attachment/forum/201801/08/021138qlwja5t5mtbhhu2a.jpg)

### Why havn't we used object detection methods like yolo/haar cascades/SSD?
At first, we tried to find (unsuccessfully) a trained weights for haar cascades.
Then, we tried to train a haar cascade for detecting trees, but it didn't fit to our goal.

We also tried to use [SSD](https://arxiv.org/abs/1512.02325)
 (Single Shot Multi-box Detection), but SSD isn't doing really well in real time on our hardware (for 30 FPS minimum).

After that, we tried to use YoloV3, Yolo could've been great for detecting an object in real time. 
We decided to train a custom object detector but we had a lot of issues with YoloV3, C++ and Python.
So, we searched for a pre-trained weights and found weights for 9000+ object (with a lot of trees type, perfect for our mission) 
but it also wasn't fast enough (for 30 FPS minimum, with our hardware).


Finally, we decideed to try some image processing manipulations with OpenCV in order to detect a specific range of brown.
The best method we found was detecting brown contours using HSV.
At the beginning we got a lot of detection, noise. So, we tried to minimize the noise but it wasn't good enough due to over detection.
After testing, and with the help of Dr. Ben-Moshe we found that when the drone is about to crash into a tree, the tree is 
detected from bottom up. we started with a simple model which is described below.

### HSV 
![alt text](https://upload.wikimedia.org/wikipedia/commons/3/33/HSV_color_solid_cylinder_saturation_gray.png)
HSV is a Hue Saturation Value(Brightness). HSV is defined in a way that is similar to how humans perceive color. 
It's based on three values: hue, saturation, and value. This color space describes colors (hue or tint) in terms of 
their shade (saturation or amount of gray) and their brightness value. Some color pickers use the acronym HSB, which 
substitutes the term brightness for value, but HSV and HSB refer to the same color model.
a short explanation from [lifewire](https://www.lifewire.com/what-is-hsv-in-design-1078068). 

After a lot of testing we found out that the best result for us (in outdoor gardens, at sunny days):  
* H range is 10 - 20.
* S range is 20 - 150.
* V(B) range is 20 - 100.

Our [brown detector](detect_model/brown_detection.py) is an implementation of HSV brown detector with OpenCV.

![alt text](https://imgur.com/6PA03ER)


## Future research
## H5 How to detect a pop up object?


## Python
use Python 3.* [download here](https://www.python.org/downloads/).

## Requirements
* keyboard
* av
* pykalman
* pygame
* matplotlib
* opencv-python
* numpy

## Usage
* Clone our project from github:  
````bash
git clone https://github.com/MatufA/drone-autonomous-escape.git
````  
* Install requirements:
```bash
pip3 install -r requirements.txt
```
* Run the project:  
```bash
python3 -m drone_autonomous_escape
```
## OpevCV Installation on Windows
See instruction [here.](https://www.learnopencv.com/install-opencv3-on-windows/)

## Authors
* **Amit Nuni** - *Autonomous Drone project* - [Profile](https://github.com/nunii)
* **Adiel Matuf** - *Autonomous Drone project* - [Profile](https://github.com/matufa)

## License
This project is licensed under the GNU License - see the [LICENSE](LICENSE) file for details.

## Credits
[ofikodar](https://github.com/ofikodar) for using his repository [drone-auto-landing](https://github.com/ofikodar/drone-auto-landing)
