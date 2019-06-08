# drone-autonomous-escape
Our project focuses on a "DJI Tello" drone, making it autonomously evade obsticles.
We focused on evading trees, by processing the video from the drone at real time, and built an algorithm which will make it avoid the trees.

![alt text](https://forum44.djicdn.com/data/attachment/forum/201801/08/021138qlwja5t5mtbhhu2a.jpg)

### why havn't we used object detection methods like yolo/haar cascades/SSD?
At first, we tried to find (unsuccessfully) a trained weights for haar cascades.
So, we tried to train a haar cascade for detecting trees, but it's isn't fit to our goal.

Then, we try to use SSD, but SSD isn't doing really well in real time. (for 30 FPS minimum, with our hardware)

After that, we try to useYoloV3, Yolo could've been great for detect an object in real time. 
We decide to train our costume object but we had a lot of problem with YoloV3, C++ and Python.
So, we look for a weight and found a weight for 9000+ object (with a lot of tree type, perfect for our mission) 
but it also wasn't fast enough. (for 30 FPS minimum, with our hardware)


Finally, we decide to try using HSV to detect a specific range of brown.
In the start we get a lot of detection, noise. So, we try to minimize the noise with Opencv but it wasn't good enough.
After testing and with the help of Dr. Boaz we found that when the drone is about to crash into a tree the tree is 
detect from bottom up. we start with a simple model. (describe below)

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
