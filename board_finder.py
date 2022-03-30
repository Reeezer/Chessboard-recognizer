from itertools import count
from telnetlib import DEBUGLEVEL
import cv2
import numpy as np
import math

debugLevel = 0  # display images if debugLevel = 1
counter = 0


def cropImg(img, x, y, w, h):
    return img[y:y+h, x:x+w]


def findValidContours(imgTresh, areaMin, areaMax, drawOnImg=None):
    global counter, debugLevel
    contours, hierarchy = cv2.findContours(imgTresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # cv2.CHAIN_APPROX_NONE stores all coords unlike SIMPLE, cv2.RETR_EXTERNAL

    if debugLevel == 1 and isinstance(drawOnImg, np.ndarray):
        imgCpy = drawOnImg.copy()

    valid_cnts = []
    for c in contours:
        area = cv2.contourArea(c)
        if area > areaMin and area < areaMax:
            valid_cnts.append(c)

            # draw centers
            M = cv2.moments(c)
            cX = int(M["m10"] / M["m00"])
            cY = int(M["m01"] / M["m00"])
            if debugLevel == 1 and isinstance(drawOnImg, np.ndarray):
                cv2.circle(imgCpy, (cX, cY), 5, (0, 0, 255), -1)

    if debugLevel == 1 and isinstance(drawOnImg, np.ndarray):
        cv2.drawContours(imgCpy, valid_cnts, -1, (0, 255, 0), 2)
        cv2.imshow(f"img {counter}", imgCpy)
        counter += 1

    return valid_cnts


def cropBoardOut_Contours(img):

    H_low = (11/255)*180
    H_high = (35/255)*180
    HUE_MIN = (H_low, 0, 0)
    HUE_MAX = (H_high, 255, 255)

    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    hsvThresh = cv2.inRange(hsv, HUE_MIN, HUE_MAX)

    valid_cnts = findValidContours(hsvThresh, 100000, 200000, img)

    if len(valid_cnts) != 1:
        print(f"Error: Found {len(valid_cnts)} boards in image")
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        exit(-1)

    boardCnt = valid_cnts[0]
    x, y, w, h = cv2.boundingRect(boardCnt)
    return cropImg(img, x, y, w, h)


def cropSquareOut_Contours(croppedBoard):
    gray = cv2.cvtColor(croppedBoard, cv2.COLOR_BGR2GRAY)

    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))  # <-----
    morphed = cv2.dilate(gray, kernel, iterations=1)

    # find canny edge
    foundThreash = 220
        # to pick only black squares
    thresh = cv2.inRange(morphed,  foundThreash, foundThreash+50)

    edged_wide = cv2.Canny(thresh, 10, 200, apertureSize=3)



    valid_cnts = findValidContours(thresh, 2000, 4000, croppedBoard)

    squareSize = 47
    croppedSquares = []
    for sY in range(0, 8):
        for sX in range(0, 8):
            xP = sX * squareSize
            yP = sY * squareSize
            croppedSquares.append(
                cropImg(croppedBoard, xP, yP, squareSize, squareSize))
    return croppedSquares


def getBoardCoords(img):
    global counter, debugLevel

    cropedImg = cropBoardOut_Contours(img)
    

    cropedSquares = cropSquareOut_Contours(cropedImg)

    if debugLevel == 1:
        for s in cropedSquares:
            cv2.imshow(f"img {counter}", s)
            counter += 1
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    return cropedSquares


def imageResize(orgImage, resizeFact):
    dim = (int(orgImage.shape[1]*resizeFact),
           int(orgImage.shape[0]*resizeFact))  # w, h
    return cv2.resize(orgImage, dim, cv2.INTER_AREA)


if __name__ == "__main__":
    #img = imageResize(cv2.imread("Board_Examples/medium.PNG",cv2.IMREAD_GRAYSCALE),0.5)
    img = imageResize(cv2.imread("Board_Examples/medium2.png"), 0.5)

    getBoardCoords(img)
