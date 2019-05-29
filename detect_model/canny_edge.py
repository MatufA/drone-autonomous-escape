import cv2


def canny_edge(title='Test', path=r"E:\Projects\drone-autonomous-escape\detect_model\1.mp4"):
    """a Canny edge detector.

    :param title: a window title.
    :param path: a path to video file (0 for camera).
    """
    # set a window name.
    cv2.namedWindow(title)
    # open video.
    cap = cv2.VideoCapture(path)
    # start a window thread.
    cv2.startWindowThread()
    # do while there are a streams.
    while cap.isOpened():
        # get frame and return value (True for success, othrwise False).
        ret, frame = cap.read()
        # if the frame is error end, otherwise do.
        if ret:
            # frame to gray scale.
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            # use Canny edge.
            edges = cv2.Canny(gray, 150, 200, apertureSize=3)
            # show results.
            cv2.imshow(title, edges)
            # press 'q' to exit.
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break
    # release video stream.
    cap.release()
    # destroy all open windows.
    cv2.destroyAllWindows()


#if __name__ == '__main__':
   # canny_edge()
