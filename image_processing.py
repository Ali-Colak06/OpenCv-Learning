import numpy as np
import cv2

image = cv2.imread('assets/indir.jpg', 1)

image_half_sized = cv2.resize(image, None, fx=0.5, fy=0.5)

image_turned = cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)

image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

image_edges = cv2.Canny(image_gray, 100, 200)




cv2.imshow('Original Image', image)
cv2.imshow('Half Sized Image', image_half_sized)
cv2.imshow('Rotated Image', image_turned)
cv2.imshow('Grayscale Image', image_gray)
cv2.imshow('Edge Detected Image', image_edges)
cv2.waitKey(0)
cv2.destroyAllWindows()
