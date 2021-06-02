import cv2
cam = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cam.isOpened():
    raise IOError("Cannot open webcam")

while True:
    ret, frame = cam.read()
    frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    cv2.imshow('Input', frame)
    c = cv2.waitKey(1)
    if c == 27:
        break

cam.release()
cv2.destroyAllWindows()
