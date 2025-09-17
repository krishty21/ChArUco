import cv2
import numpy as np
SQUARES_W  = 2
SQUARES_H  = 2
SQUARE_MM  = 40
MARKER_MM  = 20
ARUCO_DICT = cv2.aruco.DICT_6X6_250
class CharucoBig:
    def __init__(self):
        self.aruco_dict = cv2.aruco.getPredefinedDictionary(ARUCO_DICT)
        self.board = cv2.aruco.CharucoBoard_create(
            SQUARES_W, SQUARES_H,
            SQUARE_MM/1000, MARKER_MM/1000,
            self.aruco_dict
        )
        self.params = cv2.aruco.DetectorParameters_create()
        board_img = self.board.draw((SQUARES_W*100, SQUARES_H*100))
        cv2.imwrite('board.png', board_img)
        print('board.png saved – print it (no scaling) and hold in front of camera.')
    def detect(self, img):
        grey = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        corners, ids, _ = cv2.aruco.detectMarkers(grey, self.aruco_dict, parameters=self.params)
        status = "No markers"
        charuco_corners = charuco_ids = None
        if ids is not None and len(ids):
            ok, charuco_corners, charuco_ids = cv2.aruco.interpolateCornersCharuco(
                corners, ids, grey, self.board
            )
            status = "BOARD DETECTED" if ok and len(charuco_corners) >= 4 else "Few corners"
        vis = img.copy()
        if ids is not None:
            cv2.aruco.drawDetectedMarkers(vis, corners, ids)
        if charuco_corners is not None:
            cv2.aruco.drawDetectedCornersCharuco(vis, charuco_corners, charuco_ids)
        colour = (0, 255, 0) if status == "BOARD DETECTED" else (0, 165, 255)
        cv2.putText(vis, status, (30, 80), cv2.FONT_HERSHEY_SIMPLEX, 2.2, colour, 6)
        return vis
    def handle_key(self, k):
        if k == ord('q') or k == 27: return False
        return True

def main():
    detector = CharucoBig()
    cap = cv2.VideoCapture(0)
    if not cap.isOpened(): cap.open(0)
    if not cap.isOpened(): print("Camera fail"); return
    WIN_NAME = "ChArUco Board – BIG"
    cv2.namedWindow(WIN_NAME, cv2.WINDOW_NORMAL)
    cv2.setWindowProperty(WIN_NAME, cv2.WND_PROP_FULLSCREEN, cv2.WINDOW_FULLSCREEN)
    print("Fullscreen.  q or ESC to quit.")
    while True:
        ret, frame = cap.read()
        if not ret or frame is None: continue
        vis = detector.detect(frame)
        vis = cv2.resize(vis, (0, 0), fx=2.0, fy=2.0)
        cv2.imshow(WIN_NAME, vis)
        if cv2.waitKey(1) & 0xFF in (ord('q'), 27): break
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
