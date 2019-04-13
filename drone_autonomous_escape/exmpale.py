from drone_autonomous_escape import TrackObject, DroneVideo, KeyboardFly
from tello_api import Tello
import threading
import time
# using library keyboard
import keyboard
import cv2

drone = Tello()

drone.connect()
drone.wait_for_connection(60.0)
drone.land()

KF = KeyboardFly(drone)
VID = DroneVideo(drone)
tracker = TrackObject(drone)


def route():
    if KF.controller_on:
        tracker.reach_goal = False
    while not KF.controller_on:
        tracker.main()
        time.sleep(0.01)


def down():
    while True:

        if not tracker.fast_land and not KF.controller_on:
            tracker.height_deter(30)
        time.sleep(0.1)


tracker.set_export_data("test_j")
VID.set_export_vid("test_j ")

while True:
    VID.show_vid()
    tracker.is_new(VID.is_new())
    tracker.update_coords(VID.get_coords())
    tracker.export_data()
    # if key 'q' is pressed
    if keyboard.is_pressed('1'):
        if not KF.controller_on:
            drone.takeoff()
            KF.set_text("Take Off")
    # if key 'q' is pressed
    elif keyboard.is_pressed('2'):
        if not KF.controller_on:
            drone.land()
            KF.set_text("landing")
    # if key 'q' is pressed
    elif keyboard.is_pressed('3'):
        threading.Thread(target=down).start()
    # if key 'q' is pressed
    elif keyboard.is_pressed('4'):
        threading.Thread(target=route).start()
        KF.set_text("Auto pylot")
    elif keyboard.is_pressed('5'):
        KF.start_control()
        KF.set_text("keyboard control")
    elif keyboard.is_pressed('x'):
        KF.set_text("End mission")
        break
    if tracker.spot_target():
        KF.set_text("spoting target"
                    "press 4 to auto pylot")

        # KF.main()
    # print("here")

    # VID.show_vid()l
drone.land()
cv2.destroyAllWindows()
