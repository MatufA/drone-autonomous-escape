from drone_autonomous_escape import DroneVideo, KeyboardFly
from tello_api import Tello
import keyboard
import cv2


def main():
    drone = Tello()

    drone.connect()
    drone.wait_for_connection(60.0)
    drone.land()

    kf = KeyboardFly(drone)
    vid = DroneVideo(drone)
    vid.set_export_vid("test_j ")

    while True:
        vid.show_vid()
        # if key '1' is pressed
        if keyboard.is_pressed('1'):
            if not kf.controller_on:
                drone.takeoff()
                kf.set_text("Take Off")
        # if key '2' is pressed
        elif keyboard.is_pressed('2'):
            if not kf.controller_on:
                drone.land()
                kf.set_text("landing")
        elif keyboard.is_pressed('5'):
            kf.start_control()
            kf.set_text("keyboard control")
        # if key 'x' is pressed
        elif keyboard.is_pressed('x'):
            kf.set_text("End mission")
            break

    drone.land()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
