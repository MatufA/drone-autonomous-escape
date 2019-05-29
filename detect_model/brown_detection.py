import cv2
import numpy as np

cap = cv2.VideoCapture('1.mp4')
width = cap.get(3)   # float
height = cap.get(4)  # float
min_x, min_y = width, height
max_x = max_y = 0

print(width, height)

sensitivity = 25



while True:
    _, frame = cap.read()
    blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
    # GREEN
    lower_green = np.array([[60 - sensitivity, 50, 50]])  # lower bound np.array([38, 86, 0]) # BLUE
    upper_green = np.array([60 + sensitivity, 200, 200])  # upper bound np.array([121, 255, 255]) # BLUE

    # BROWN H value 10-20 seems good. also S value 20-150 seems fine.
    lower_brown = np.array([10, 20, 20])
    upper_brown = np.array([20, 150, 100])
    mask = cv2.inRange(hsv, lower_brown, upper_brown)
    contours, _ = cv2.findContours(mask, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

    for contour in contours:
        # cv2.drawContours(frame, contour, -1, (0, 0, 255), 3)
        (x, y, w, h) = cv2.boundingRect(contour)
        min_x, max_x = min(x, min_x), max(x + w, max_x)
        min_y, max_y = min(y, min_y), max(y + h, max_y)
        if w > 50 and h > 50:
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    if max_x - min_x > 0 and max_y - min_y > 0:
        cv2.rectangle(frame, (min_x, min_y), (max_x, max_y), (255, 0, 0), 2)

    cv2.rectangle(frame, (100, 60), (540, 346), (255, 255, 0), 3)
    cv2.imshow("Frame", frame)
    cv2.imshow("Mask", mask)
    key = cv2.waitKey(1)
    if key == 27:
        break

cap.release()
cv2.destroyAllWindows()