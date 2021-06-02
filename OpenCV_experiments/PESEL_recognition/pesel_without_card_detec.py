import cv2
import pytesseract
from PIL import Image
import numpy as np
import imutils


def search_pesel(image_name) :
    img = Image.open(image_name)
    image = np.array(img)
    card = imutils.resize(image, height=600)
    # Set up to search the PESEL
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    
    #Preprocessing the picture
    gray = cv2.cvtColor(card, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (3, 3), 0)
    blackhat = cv2.morphologyEx(gray, cv2.MORPH_BLACKHAT, rectKernel)
    gradX = cv2.Sobel(blackhat, ddepth=cv2.CV_32F, dx=1, dy=0, ksize=-1)
    gradX = np.absolute(gradX)
    (minVal, maxVal) = (np.min(gradX), np.max(gradX))
    gradX = (255 * ((gradX - minVal) / (maxVal - minVal))).astype("uint8")
    gradX = cv2.morphologyEx(gradX, cv2.MORPH_CLOSE, rectKernel)
    thresh = cv2.threshold(gradX, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Finding coutours and sorting them
    cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key=cv2.contourArea, reverse=True)
    
    for c in cnts:
        (x, y, w, h) = cv2.boundingRect(c)
        ar = w / float(h)
        crWidth = w / float(gray.shape[1])
        
        # Checking if the aspect ratio and the bounding box width can correspond to the PESEL number
        if (ar>5 and ar<7) and (crWidth > 0.12 and crWidth<0.15):
            pX = int((x + w) * 0.03)
            pY = int((y + h) * 0.03)
            (x, y) = (x - pX, y - pY)
            (w, h) = (w + (pX * 2), h + (pY * 2))
    		# Extracting the PESEL number and drawing a box around it on the card
            student_number = card[y:y + h, x:x + w].copy()
            cv2.rectangle(card, (x, y), (x + w, y + h), (0, 255, 0), 2)
            after_process= Image.fromarray(student_number)
            result = pytesseract.image_to_string(student_number)
            arr = result.split('\n')[0:-1]
            result = '\n'.join(arr)
            if result.isdecimal() :
                print("PESEL = ", result) 
                after_process.save('pesel.jpg')
                
if __name__=="__main__":
    search_pesel("2.jpg")
        
