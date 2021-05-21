import cv2
import pytesseract
from PIL import Image
import numpy as np
import imutils

img = Image.open("3.jpg")
image = np.array(img)

rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
sqKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (21, 21))

image = imutils.resize(image, height=600)
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (3, 3), 0)
blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
gradX = np.absolute(gradX)
(minVal, maxVal) = (np.min(gradX), np.max(gradX))
gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
# find contours in the thresholded image and sort them by their
# size
cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)
cnts = sorted(cnts, key=cv2.contourArea, reverse=True)


for c in cnts:
	# compute the bounding box of the contour and use the contour to
	# compute the aspect ratio and coverage ratio of the bounding box
	# width to the width of the image
    (x, y, w, h) = cv2.boundingRect(c)
    ar = w / float(h)
    # print(name)
    # print("ar =",ar)
    crWidth = w / float(gray.shape[1])
    #print("cr =",crWidth)
	# check to see if the aspect ratio and coverage width are within
	# acceptable criteria
    if (ar>5 and ar<7) and (crWidth > 0.12 and crWidth<0.15):
		# pad the bounding box since we applied erosions and now need
		# to re-grow it
        pX = int((x + w) * 0.03)
        pY = int((y + h) * 0.03)
        (x, y) = (x - pX, y - pY)
        (w, h) = (w + (pX * 2), h + (pY * 2))
		# extract the ROI from the image and draw a bounding box
		# surrounding the MRZ
        student_number = image[y:y + h, x:x + w].copy()
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv2.imshow("Student number",student_number)
        cv2.waitKey(0);

after_process= Image.fromarray(student_number)
after_process.save('student_id.jpg')
result = pytesseract.image_to_string(student_number)

arr = result.split('\n')[0:-1]
result = '\n'.join(arr)
print("Student number = ", result) 