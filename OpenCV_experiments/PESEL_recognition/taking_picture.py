import cv2
import pesel_detection as det
cam = cv2.VideoCapture(0,cv2.CAP_DSHOW)

cv2.namedWindow("test")

while True:
    ret, frame = cam.read()
    if not ret:
        print("failed to grab frame")
        break
    cv2.imshow("test", frame)
    
    k = cv2.waitKey(1)
    if k%256 == 32:
        # SPACE pressed
        img_name = "opencv_frame.png"
        cv2.imwrite(img_name, frame)
        print("{} written!".format(img_name))
        print("Escape hit, closing...")
        cam.release()
        cv2.destroyAllWindows()
        break
    


det.opti_detection(img_name)