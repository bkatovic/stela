import cv2
import pytesseract
from PIL import Image
import numpy as np
import imutils

class CardDetection:
    def __init__(self):
        self.image = None
        self.detected = 0  
        self.pesel=0

def init(image_name):
    img = Image.open(image_name)
    image = np.array(img)
    #image=cv2.imread(image_name)
    image = imutils.resize(image, height=600)
    return image

def search_card_by_chip(image) :
    card=CardDetection()
    rectKernel = cv2.getStructuringElement(cv2.MORPH_RECT, (13, 5))
    
    #Preprocessing the picture
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
        #print("ar=",ar)
        #print("cr=",crWidth)
        if (ar>1 and ar<1.5) and (crWidth > 0.10 and crWidth<0.16):
            #print("ar=",ar)
            #print("cr=",crWidth)
			# pad the bounding box since we applied erosions and now need
			# to re-grow it
            pX = int((x + w) * (ar/3))
            pY = int((y + h) * (ar/2.3))
            (x, y) = (x - pX, y - pY)
            (w, h) = (w + (pX * 7), h + (pY * 3)-70)
            print("w=",w)
     			# extract the ROI from the image and draw a bounding box
     			# surrounding the MRZ
            card.image = image[y:y + h, x:x + w].copy()
            cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.imshow("card by chip", card.image)
            #cv2.imshow("Image", image)
            #cv2.waitKey(0)
           # cv2.destroyAllWindows()
            if card.image is None:
                card.detected=0
            else:
                card.detected=1
            return card
                
def search_card_by_contours(image):
    original = image.copy()
    card=CardDetection()
     
    # Edge detection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.GaussianBlur(gray, (5, 5), 0)
    edged = cv2.Canny(gray, 75, 200)
     
    #cv2.imshow("Edged picture", edged)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
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
    
    cv2.drawContours(original, [screenCnt], -1, (0, 255, 0), 2)
    #cv2.imshow("Outline", image)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
    
    #Cropping the original image to obtain the card image
    (x, y, w, h) = cv2.boundingRect(c)
    if w>h :
        pX = int((x + w) * 0.03)
        pY = int((y + h) * 0.03)
        (x, y) = (x - pX, y - pY)
        (w, h) = (w + (pX * 2), h + (pY * 2))
        card.image = original[y:y + h, x:x + w].copy()
        cv2.rectangle(image, (x, y), (x + w, y + h), (0, 255, 0), 2)
        #cv2.imshow("Card",card.image)
        #cv2.waitKey(0)
        card.detected=1
    return card

def search_pesel(card) :
    card = imutils.resize(card, height=600)
    #cv2.imshow("Carte pour recherche", card)
    #cv2.waitKey(0)
    #cv2.destroyAllWindows()
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
                #cv2.imshow("Outline", student_number)
                #cv2.waitKey(0)
                #cv2.destroyAllWindows()
                print("PESEL = ", result) 
                after_process.save('pesel.jpg')
                return 1
                break
    return 0
                
def opti_detection(image_name):
    image=init(image_name)
    card=search_card_by_contours(image)
    if card.detected==1:
        #print("card detected with contours")
        search_pesel(card.image)
    else :
        #print("try with chip")
        card=search_card_by_chip(image)
        #print("card detected with chip")
        search_pesel(card.image)

    
    
    
