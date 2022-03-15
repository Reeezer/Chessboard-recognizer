import cv2
import numpy as np
import math


def cropImg(img,x,y,w,h):
    return img[y:y+h, x:x+w]

def getBoardCoords(img):
    x = 0
    y = 0
    h = 100
    w = 100
    
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    
    H_low = (11/255)*180
    H_high = (35/255)*180
    HUE_MIN = (H_low,0,0)
    HUE_MAX = (H_high,255,255)
    
    hsvThresh = cv2.inRange(hsv,HUE_MIN,HUE_MAX)
    
    edged_board = cv2.Canny(hsvThresh, 10, 200, apertureSize=3)
    
    contours, hierarchy = cv2.findContours(
        hsvThresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # cv2.CHAIN_APPROX_NONE stores all coords unlike SIMPLE, cv2.RETR_EXTERNAL

    
    boardCntImg = img.copy()
    valid_cnts = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > 100000 and area < 200000:
            valid_cnts.append(c)

            # draw centers 
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(boardCntImg, (cX, cY), 5, (0, 0, 255), -1)

    cv2.drawContours(boardCntImg, valid_cnts, -1, (0, 255, 0), 2)
    
    if len(valid_cnts) != 1:
        print(f"Error: Found {len(valid_cnts)} boards in image")
        cv2.imshow(f"board contours",boardCntImg)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(-1)
    
    boardCnt = valid_cnts[0]
    x,y,w,h = cv2.boundingRect(boardCnt)
    cropedImg = cropImg(img,x,y,w,h)
    
    
    
    gray = cv2.cvtColor(cropedImg, cv2.COLOR_BGR2GRAY)
    
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2)) # <-----                                                                             
    morphed = cv2.dilate(gray, kernel, iterations=1)

    
    
    # find canny edge
    foundThreash = 220 # Found this value by testing
    thresh = cv2.inRange(morphed,  foundThreash, foundThreash+15)  # to pick only black squares
    
    edged_wide = cv2.Canny(thresh, 10, 200, apertureSize=3)
    

    # find Contours
    contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # cv2.CHAIN_APPROX_NONE stores all coords unlike SIMPLE, cv2.RETR_EXTERNAL


    cntImg = gray.copy()

    minArea, maxArea = 2000, 4000

    valid_cnts = [] 
    for c in contours:
        area = cv2.contourArea(c)
        if area > minArea and area < maxArea:
            valid_cnts.append(c)

            # draw centers 
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            cv2.circle(cntImg, (cX, cY), 5, (0, 0, 255), -1)


    cv2.drawContours(cntImg, valid_cnts, -1, (0, 255, 0), 2)
    
    squareSize = round(math.sqrt(sum([cv2.contourArea(x) for x in valid_cnts]) / len(valid_cnts)))
    croppedSquares = []
    for sX in range(0,8):
        for sY in range(0,8):
            xP = sX * squareSize
            yP = sY * squareSize
            croppedSquares.append(cropImg(cropedImg,xP,yP,squareSize,squareSize))

    return croppedSquares

    cv2.imshow(f"board contours",boardCntImg)
    cv2.imshow('cropped',cropedImg)
    #cv2.imshow('threshold', thresh)
    #cv2.imshow('morphed', morphed)
    cv2.imshow('canny edge', edged_wide)
    cv2.imshow('contour', cntImg)
    cv2.waitKey(0)

    cv2.destroyAllWindows()
    
    
    return x,y,w,h

def imageResize(orgImage, resizeFact):
    dim = (int(orgImage.shape[1]*resizeFact),       
           int(orgImage.shape[0]*resizeFact))  # w, h
    return cv2.resize(orgImage, dim, cv2.INTER_AREA)


if __name__ == "__main__":
    #img = imageResize(cv2.imread("Board_Examples/medium.PNG",cv2.IMREAD_GRAYSCALE),0.5)
    img = imageResize(cv2.imread(("Board_Examples/medium2.png")), 0.5)

    getBoardCoords(img)
    
    