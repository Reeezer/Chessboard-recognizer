import os
import cv2
import time
import re

from pynput.keyboard import Key, Listener,KeyCode
  
color = ""
piece = ""


def waitForColor(key):
    global color
    print('\nYou Entered {0}'.format( key))
    
    if key.char == "b":
        color = "black" #Black
        return False
    elif key.char == "w":
        color = "white"
        return False
    
def waitForPiece(key):
    global piece
    print('\nYou Entered {0}'.format( key))
    
    if key.char == "b":
        piece = "bishop" #Black
        return False
    elif key.char == "k":
        piece = "king"
        return False
    elif key.char == "n":
        piece = "knight"
        return False
    elif key.char == "p":
        piece = "pawn"
        return False
    elif key.char == "q":
        piece = "queen"
        return False
    elif key.char == "r":
        piece = "rook"
        return False
    


  
# Collect all event until released


def getImages(inputDir):
    images = []

    for root, dirs, files in os.walk(inputDir):
        for file in files:
            #print(file)
            images.append(cv2.imread(inputDir + "/" + file))
    return images
    

def labelImages(images,outputDir):
    if not os.path.exists(outputDir):
        os.makedirs(outputDir)
        counter = 0
    else:
        filesArray = []
        for root, dirs, files in os.walk(outputDir):
            for file in files:
                filesArray.append(file)
                
        counter = len(filesArray)
    
    for i, im in enumerate(images):
        cv2.imshow(f"Image {i}",im)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        
        print("What color is this piece?: ")
        with Listener(on_press = waitForColor) as listener:   
            listener.join()
        print("What piece is this?: ")
        with Listener(on_press = waitForPiece) as listener:   
            listener.join()
        cv2.destroyAllWindows()
        cv2.imwrite(f"{outputDir}/{color}_{piece}_{counter}.png",im)
        counter += 1
        
        

        
if __name__ == "__main__":
    images = getImages(".\pieces")
    labelImages(images,"labeled")
    cv2.waitKey(0)
    cv2.destroyAllWindows()