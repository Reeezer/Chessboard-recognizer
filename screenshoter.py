import os
from pynput.keyboard import Key, Listener,KeyCode
import numpy as np
import cv2
import pyautogui


outputDir = "unlabeled"

counter = 0
if not os.path.exists(outputDir):
    os.makedirs(outputDir)
else:
    filesArray = []
    for root, dirs, files in os.walk(outputDir):
        counter += len(files)

print(counter)

def waitForKey(key):
    global counter
    
    if key == Key.space:
        print("Screenshot")
        # take screenshot using pyautogui
        image = pyautogui.screenshot()
        
        # since the pyautogui takes as a 
        # PIL(pillow) and in RGB we need to 
        # convert it to numpy array and BGR 
        # so we can write it to the disk
        image = cv2.cvtColor(np.array(image),
                            cv2.COLOR_RGB2BGR)
        
        # writing it to the disk using opencv
        cv2.imwrite(f"{outputDir  }/{counter}.png", image)
        counter += 1
    elif key == Key.enter:
        exit(0)

with Listener(on_press = waitForKey) as listener:   
            listener.join()