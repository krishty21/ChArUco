# make_charuco_test_image.py
import cv2

SQUARES_W  = 7
SQUARES_H  = 5
SQUARE_MM  = 40
MARKER_MM  = 20
ARUCO_DICT = cv2.aruco.DICT_6X6_250

aruco_dict = cv2.aruco.Dictionary_get(ARUCO_DICT)
board = cv2.aruco.CharucoBoard_create(
    SQUARES_W, SQUARES_H,
    SQUARE_MM / 1000,
    MARKER_MM / 1000,
    aruco_dict)

DPI  = 300
A4_W = int(8.27 * DPI)  
A4_H = int(11.69 * DPI) 

img = board.draw((A4_W, A4_H))
cv2.imwrite('charuco_test.jpg', img)
print('Saved charuco_test.jpg – show it to the camera.')