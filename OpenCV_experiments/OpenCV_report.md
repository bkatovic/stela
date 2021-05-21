# OCR Report
The Optical Character Recognition (OCR) is the conversion of images containing typed, handwritten or printed text into machine-readable text. OCR is subdivided in several sub-processes as preprocessing of the image, text localization or post processing.

As part of our project, we wanted to read the PESEL from the student's card. To achieve our goal, we decided to work with several OCR tools as OpenCV or Pytesseract.

## OpenCV

OpenCV (Open Computer Vision) is an open source library dedicated to OCR. It contains several useful functionalities. First, OpenCV has some practical functions to open, display, save and modify pictures. For instance, it allows us to see the different modifications on our picture without creating and checking copies in our directory. It also has a lot of preprocessing functions to transform our original picture, allowing us to make it more readable for the rest of the process.

## Tesseract

Tesseract is an open source text recognition engine. It is compatible with many programming languages and frameworks through wrappers. In our project, we use the Python wrapper : Pytesseract. 

It is really efficient in our case because as soon as the picture is readable and focused on the PESEL, Tesseract gives us a perfect result. 

## Other tools and process

The two main parts of our process are the recognition of the card on the picture and finding the PESEL on the card. 

The first one is done by detecting edges on the picture and adding some conditions to focus on the rectangle shape of the card. When we are focused on the card, we cropp it to have a readable base for the second part : finding the PESEL.

This part is based on blob-detection. After applying some preprocessing functions, we can detect the different parts of the card. To know which one is the PESEL number, we did some experiments to find the ratio height/length of the block and the coverage ratio that is related to the size of the entire card. With that information, we are able to select the good block. Then we crop it to use pytesseract.

The other modules that we use are numpy, PIL and imutils. They are really useful to manipulate the picture.

## Limits and improvements

- The actual version of our program is able to detect the PESEL number on the polish student’s card only. It’s due to the conditions to select the PESEL block. The ratios are not the same on other cards.
- The detection is not working if the card isn’t on a dark background.
- For now, the source is a classic picture file. We could improve that to make it work with a webcam
