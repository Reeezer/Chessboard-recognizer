import sys
import math
from turtle import distance
import cv2 as cv
import numpy as np
from board_finder import imageResize
import itertools
import operator

import math

deadZone = 5
debugLevel = 1
counter = 0

def cropImg(img, x, y, w, h):
    return img[y:y+h, x:x+w]

def dot(vA, vB):
    return vA[0]*vB[0]+vA[1]*vB[1]

def ang(lineA, lineB):
    # Reshape the lines to work with function #X, Y    X Y coords
    lineA = ((lineA[0][0],lineA[0][1]),(lineA[0][2],lineA[0][3]))
    lineB = ((lineB[0][0],lineB[0][1]),(lineB[0][2],lineB[0][3]))
    # Get nicer vector form
    vA = [(lineA[0][0]-lineA[1][0]), (lineA[0][1]-lineA[1][1])]
    vB = [(lineB[0][0]-lineB[1][0]), (lineB[0][1]-lineB[1][1])]
    # Get dot prod
    dot_prod = dot(vA, vB)
    # Get magnitudes
    magA = dot(vA, vA)**0.5
    magB = dot(vB, vB)**0.5
    # Get cosine value
    cos_ = dot_prod/magA/magB
    # Get angle in radians and then convert to degrees
    angle = math.acos(dot_prod/magB/magA)
    # Basically doing angle <- angle mod 360
    ang_deg = math.degrees(angle)%360
    
    if ang_deg-180>=0:
        # As in if statement
        return round(360 - ang_deg)
    else: 
        
        return round(ang_deg)

def lengthLine(line):
    x1 = line[0][0]
    y1 = line[0][1]
    x2 = line[0][2]
    y2 = line[0][3]
    return round(math.sqrt((x1-x2)**2 + (y1-y2)**2))


def accumulate(l):
    lengths = [length for ang,length in l]
    angs = [ang for ang,length in l]
    lengthToCount = {}
    for ang,length in l:
        countLengths = len(list(filter(lambda x: x >= length - deadZone and x <= length + deadZone, lengths)))
        countAngs = len(list(filter(lambda x: x >= ang - deadZone and x <= ang + deadZone, angs)))
        #count = lengths.count(length) + lengths.count(length+1) + lengths.count(length-1)
        if countLengths == 18 and length > 150:
            print(f"{countLengths} {countAngs}")
            for i in range(length - deadZone, length + deadZone):
                if lengthToCount.get(i) is None or lengthToCount[i] < countLengths:
                    lengthToCount[i] = countLengths
            

    return list(lengthToCount.keys())


       
def main(argv):
    
    default_file = 'Board_Examples/medium2.png'
    filename = argv[0] if len(argv) > 0 else default_file
    # Loads an image
    src = cv.imread(cv.samples.findFile(filename))
    src = imageResize(src,0.5)
    # Check if image is loaded fine
    if src is None:
        print ('Error opening image!')
        print ('Usage: hough_lines.py [image_name -- default ' + default_file + '] \n')
        return -1
    
    dst = cv.Canny(src, 100, 200, None, 3)
    
    # Copy edges to the images that will display the results in BGR
    cdst = cv.cvtColor(dst, cv.COLOR_GRAY2BGR)
    cdstP = np.copy(cdst)
    
    linesP = cv.HoughLinesP(dst, 1, np.pi / 180, 50, None, 50, maxLineGap=5)
    #linesP = np.array([[[200,100,500,100]],[[200,100,200,500]]])
    horizontalLine = [[0,0,100,0]]
    
    angles = [(ang(x,horizontalLine),lengthLine(x)) for x in linesP]
    angles.sort(key=lambda y: y[1])
    lengths = accumulate(angles)
    print(lengths)
    #print(ang(linesP[0],horizontalLine))
    boardLines = []
    if linesP is not None:
        for i in range(0, len(linesP)):
            lengLine = lengthLine(linesP[i])
            #print(lengLine)
            if lengLine in lengths:
                #print("found line")
                pass
                l = linesP[i][0]
                boardLines.append(l)
                cv.line(cdstP, (l[0], l[1]), (l[2], l[3]), (0,0,255), 1, cv.LINE_AA)
    
    
    cv.imshow("Source", src)
    cv.imshow("Detected Lines (in red) - Probabilistic Line Transform", cdstP)
    
    #print(f"{linesP[-1]} {linesP[-2]}")
    
    cv.waitKey()
    return 0
    
if __name__ == "__main__":
    main(sys.argv[1:])
    