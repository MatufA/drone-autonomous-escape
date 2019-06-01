import cv2
import numpy as np


def track_obj(frame, min_x, min_y, max_x, max_y):
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), cv2.BORDER_DEFAULT)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

    # BROWN H value 10-20 seems good. also S value 20-150 seems fine.
    lower_brown = np.array([10, 20, 20])
    upper_brown = np.array([20, 150, 100])

    mask = cv2.inRange(hsv, lower_brown, upper_brown)
    kernel = np.ones((3, 3), np.uint8)
    mask = cv2.erode(mask, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        area = cv2.contourArea(contour)
        approx = cv2.approxPolyDP(contour, 0.01 * cv2.arcLength(contour, True), True)
        if area > 200:
            # cv2.drawContours(frame, [approx], -1, (0, 0, 255), 5)
            (x, y, w, h) = cv2.boundingRect(approx)
            min_x, max_x = min(x, min_x), max(x + w, max_x)
            min_y, max_y = min(y, min_y), max(y + h, max_y)

            if w > 50 and h > 50:
                cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
    cv2.imshow("Mask", mask)
    return frame


def brown_detect(title='Test', path=r"2.mp4"):
    cv2.namedWindow(title)
    cap = cv2.VideoCapture(path)
    width = cap.get(3)  # float
    height = cap.get(4)  # float
    min_x, min_y = width, height
    max_x = max_y = 0

    target_x_min = round(width) // 4
    target_x_max = 3 * round(width) // 4
    target_y_min = 0
    target_y_max = round(height)

    while True:
        ret, frame = cap.read()
        if ret:
            frame = track_obj(frame=frame, min_x=min_x, min_y=min_y, max_x=max_x, max_y=max_y)
            # if max_x - min_x > 0 and max_y - min_y > 0:
            #     cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

            cv2.rectangle(frame, (target_x_min, target_y_min), (target_x_max, target_y_max), (255, 255, 0), 3)
            cv2.imshow(title, frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
        else:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    brown_detect()
