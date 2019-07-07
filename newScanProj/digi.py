from transform import four_point_transform
from skimage.filters import threshold_local
import numpy as np
import cv2
import imutils
import shutil

def scan(imgFile):
    image = cv2.imread(imgFile)
    ratio = cv2.imread(imgFile).shape[0]/500.0
    orig = image.copy()
    image = imutils.resize(image,height = 500)
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    gray = cv2.medianBlur(gray,5)
    edged = cv2.Canny(gray,75,200)
    cnts = cv2.findContours(edged.copy(),cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
    cnts = imutils.grab_contours(cnts)
    cnts = sorted(cnts,key = cv2.contourArea,reverse = True)[:5]
    for c in cnts:
        perimeter = cv2.arcLength(c,True)
        approx = cv2.approxPolyDP(c,0.02*perimeter,True)
        if len(approx) == 4:
            screenCnt = approx
            break
    warped = four_point_transform(orig,screenCnt.reshape(4,2)*ratio)
    warped = cv2.cvtColor(warped,cv2.COLOR_BGR2GRAY)
    T = threshold_local(warped,11,offset = 10,method = "gaussian")
    warped = (warped > T).astype("uint8")*255
    cv2.imwrite('newImage.png',warped)
    shutil.copy('newImage.png','static/uploads/converted/')
