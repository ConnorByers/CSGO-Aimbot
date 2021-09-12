import numpy as np
import cv2
from mss import mss
from PIL import Image
from time import time
from pynput import keyboard
import math

# 275 x 850
bounding_box = {'top': 150, 'left': 150, 'width': 1000, 'height': 425}

sct = mss()
sct_img = np.array(sct.grab(bounding_box))
cur_time = time()

model = cv2.CascadeClassifier('cascade/cascade.xml')

def isValidCounterTerroristColor(color, corner):
    r, g, b = int(color[2]), int(color[1]), int(color[0])
    c_r, c_g, c_b = int(corner[2]), int(corner[1]), int(corner[0])
    hsp = math.sqrt( 0.299*r*r + 0.587*g*g + 0.114*b*b )
    corner_hsp = math.sqrt( 0.299*c_r*c_r + 0.587*c_g*c_g + 0.114*c_b*c_b )
    if hsp < 30 and (corner_hsp+1)/(hsp+1) > 2 and ((abs(2*r - b - g) < 15) or (abs(b - 2 * r) < 10 and abs(b - 2 * g) < 10)):
        return True
    return False

def isCounterTerrorist(img, x, y, w, h):
    mid_pos_x, mid_pos_y = x + w // 2 , y + h // 2
    if y > 30 and y < 350 and isValidCounterTerroristColor(img[mid_pos_y, mid_pos_x], img[mid_pos_y, x]):
        return True
    return False

def filterRectangles(rec):
    new_rec = []
    for (x, y, w, h) in rec:
        if isCounterTerrorist(sct_img, x, y, w, h):
            new_rec.append((x, y, w, h))
    return new_rec

def drawRectangles(rec, sct_img):
    for (x, y, w, h) in rec:
        top_left_point = (x, y)
        bottom_right_point = (x + w, y + h)
        cv2.rectangle(sct_img, top_left_point, bottom_right_point, (0, 255, 0))

while True:
    sct_img = np.array(sct.grab(bounding_box))

    rec = model.detectMultiScale(sct_img)
    
    rec = filterRectangles(rec)

    rec = cv2.groupRectangles(np.concatenate((rec, rec)).tolist(),0,eps=0.03)[0]
    drawRectangles(rec, sct_img)
    
    cv2.imshow('screen', sct_img)
    cur_time = time()
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
