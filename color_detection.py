import numpy as np
import cv2 as cv

def dummy(x): # empty func for trackbars
    pass

cv.namedWindow("Trackbars")

cv.createTrackbar("Lower-H", "Trackbars", 0, 179, dummy)
cv.createTrackbar("Lower-S", "Trackbars", 0, 255, dummy)
cv.createTrackbar("Lower-V", "Trackbars", 0, 255, dummy)
cv.createTrackbar("Upper-H", "Trackbars", 179, 179, dummy)
cv.createTrackbar("Upper-S", "Trackbars", 255, 255, dummy)
cv.createTrackbar("Upper-V", "Trackbars", 255, 255, dummy)

camera = cv.VideoCapture(0)

if not camera.isOpened():
    print("Camera is not working!")
    exit()

kernel = np.ones((5, 5), np.uint8)

while True:
    ret, frame = camera.read()

    if not ret:
        print("Cannot read data from the frame!")
        break

    l_h = cv.getTrackbarPos("Lower-H", "Trackbars")
    l_s = cv.getTrackbarPos("Lower-S", "Trackbars")
    l_v = cv.getTrackbarPos("Lower-V", "Trackbars")
    u_h = cv.getTrackbarPos("Upper-H", "Trackbars")
    u_s = cv.getTrackbarPos("Upper-S", "Trackbars")
    u_v = cv.getTrackbarPos("Upper-V", "Trackbars")
    
    frame_hsv = cv.cvtColor(frame, cv.COLOR_BGR2HSV)
    lower_hsv_values = np.array([l_h, l_s, l_v])
    upper_hsv_values = np.array([u_h, u_s, u_v])
    
    mask = cv.inRange(frame_hsv, lower_hsv_values, upper_hsv_values)
    mask = cv.morphologyEx(mask, cv.MORPH_OPEN, kernel)
    result = cv.bitwise_and(frame, frame, mask=mask)
    contours, hierarchy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

    if (len(contours) > 0):
        max_contour = max(contours, key= cv.contourArea)
        M = cv.moments(max_contour)
        if (M["m00"] != 0):
            Cx = M["m10"] / M["m00"]
            Cy = M["m01"] / M["m00"]

            x, y, w, h = cv.boundingRect(max_contour)
            cv.rectangle(frame, (x, y), ((x + w), (y + h)), (0, 0, 255), 2)

            center_x = int(Cx)
            center_y = int(Cy)

            cv.circle(frame, (center_x, center_y), 4, (0, 0, 255), -1)


    cv.imshow("Camera", frame)
    cv.imshow("Color Detector", result)

    if (cv.waitKey(1) & 0xFF == ord("x")):
        break

camera.release()
cv.destroyAllWindows()
