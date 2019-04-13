import sys
import traceback

import keyboard
import tellopy
import av
import cv2.cv2 as cv2  # for avoidance of pylint error
import numpy
import time


count_img=0
drone = tellopy.Tello()

try:
    drone.connect()
    drone.wait_for_connection(60.0)

    retry = 3
    container = None
    while container is None and 0 < retry:
        retry -= 1
        try:
            container = av.open(drone.get_video_stream())
        except av.AVError as ave:
            print(ave)
            print('retry...')

    # skip first 300 frames
    frame_skip = 300
    while True:
        for frame in container.decode(video=0):
            if 0 < frame_skip:
                frame_skip = frame_skip - 1
                continue
            start_time = time.time()
            image = cv2.cvtColor(numpy.array(frame.to_image()), cv2.COLOR_RGB2BGR)
            image=cv2.resize(image,(300,225))
            cv2.imshow("image",image)
            cv2.waitKey(1)
            if frame.time_base < 1.0 / 60:
                time_base = 1.0 / 60
            else:
                time_base = frame.time_base
            frame_skip = int((time.time() - start_time) / time_base)
            if keyboard.is_pressed('s'):  # if key 'q' is pressed
                cv2.imwrite(str(count_img)+'.jpg', image)
                count_img+=1
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break


except Exception as ex:
    exc_type, exc_value, exc_traceback = sys.exc_info()
    traceback.print_exception(exc_type, exc_value, exc_traceback)
    print(ex)
finally:
    drone.quit()
    cv2.destroyAllWindows()


