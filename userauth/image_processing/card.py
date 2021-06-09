import cv2
import pytesseract
from PIL import Image
import numpy as np
import imutils


def detect_card(image_name):
    # Opening the picture
    img = Image.open(image_name)
    image = np.array(img)
    image = imutils.resize(image, height=600)
    original = image.copy()
     
    # Edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
     
    # cv2.imshow("Edged picture", edged)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    # Finding contours
    cnts = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts, key = cv2.contourArea, reverse = True)[:5]
     
    # Loop over the contours
    for c in cnts:
    	# Approximate the contour
    	peri = cv2.arcLength(c, True)
    	approx = cv2.approxPolyDP(c, 0.02 * peri, True)
     
    	# Contour of the card should have 4 points
    	if len(approx) == 4:
    		screenCnt = approx
    		break
    
    # cv2.drawContours(image, [screenCnt], -1, (0, 255, 0), 2)
    # cv2.imshow("Outline", image)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()
    
    #Cropping the original image to obtain the card image
    (x, y, w, h) = cv2.boundingRect(c)
    
    pX = int((x + w) * 0.03)
    pY = int((y + h) * 0.03)
    (x, y) = (x - pX, y - pY)
    (w, h) = (w + (pX * 2), h + (pY * 2))
    card = original[y:y + h, x:x + w].copy()
    cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
    # cv2.imshow("Card",card)
    # cv2.waitKey(0)
    return card

def search_pesel(image_name) :
    # Set up to search the PESEL
    card = imutils.resize(image_name, height=600)
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
                return(result) 
                # after_process.save('pesel.jpg')
                
if __name__=="__main__":
    card=detect_card("3.jpg")
    search_pesel(card)
        
