import cv2
import pytesseract
from PIL import Image
import preprocessing_functions as prep
import numpy as np

img = Image.open("student.jpg")
image = np.array(img)
data_processed=cv2.resize(image, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
after_process= Image.fromarray(data_processed)
after_process.save('student_after_process.jpg')
result = pytesseract.image_to_string(Image.open('student_after_process.jpg'))

arr = result.split('\n')[0:-1]
result = '\n'.join(arr)

print(result)