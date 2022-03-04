import cv2
import numpy as np
import math

cam = cv2.VideoCapture(2)


def recadrage1(img):
    height, width = img.shape
    recHeightMin = int(height/2)-80
    recHeightMax = int(height/2)+310
    recWidthMin = int(width/2)-300
    recWidthMax = int(width/2)+300
    return img[recHeightMin: recHeightMax , recWidthMin :recWidthMax]

def recadrage2(img):
    height, width = img.shape
    recHeightMin = int(height/2)-60
    recHeightMax = int(height/2)+75
    recWidthMin = int(width/2)-100
    recWidthMax = int(width/2)+1200
    return img[recHeightMin: recHeightMax , recWidthMin :recWidthMax]

while(True):
    ret, frame = cam.read()

    if not ret: #si on arrive à la fin de la vidéo, on recommence
        cam.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cam.read()

    img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray = recadrage1(img)  # video 1 et 2
    #gray = recadrage2(img)  # video 3
    ret, BinaryImage = cv2.threshold(gray, 100 ,255, cv2.THRESH_BINARY_INV)

    edges= cv2.Canny(BinaryImage,50 ,150, apertureSize = 3)

    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 70, minLineLength=10, maxLineGap=250)
    if lines is not None:
        for line in lines:
            x1, y1, x2, y2 = line[0]

            cv2.line(gray, (x1, y1), (x2, y2), 255, 2)
            cv2.circle(gray, (x1, y1), 4, 255, 5)
            cv2.circle(gray, (x2, y2), 4, 255, 5)
    cv2.imshow('image', gray)
    cv2.imshow('binary', BinaryImage)

    if cv2.waitKey(1) & 0xFF == ord('q'):      # on appui sur q pour continuer
        break
cam.release()
cv2.destroyAllWindows()