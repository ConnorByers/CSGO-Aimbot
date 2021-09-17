import numpy as np
import cv2
from mss import mss
from PIL import Image
from time import time
from pynput import keyboard, mouse
import math

rec = []
CROSSHAIR_POSITION = (491, 236)

cur_mouse = mouse.Controller()

def on_press(key):
    if key == keyboard.KeyCode.from_char('l'):
        if rec is not None and len(rec) == 1:
            mid_x, mid_y = getMiddlePosition(rec[0][0],rec[0][1],rec[0][2],rec[0][3])
            DIF = (mid_x - CROSSHAIR_POSITION[0], mid_y - CROSSHAIR_POSITION[1])
            cur_mouse.move(int(2.2*DIF[0]), 2*DIF[1]-35)

def on_release(key):
    pass

listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

bounding_box = {'top': 150, 'left': 150, 'width': 1000, 'height': 425}

sct = mss()
sct_img = np.array(sct.grab(bounding_box))
cur_time = time()

model = cv2.CascadeClassifier('cascade/cascade.xml')

def getMiddlePosition(x, y, w, h):
    return x + w // 2 , y + h // 2

def isValidCounterTerroristColor(color, corner):
    r, g, b = int(color[2]), int(color[1]), int(color[0])
    c_r, c_g, c_b = int(corner[2]), int(corner[1]), int(corner[0])
    hsp = math.sqrt( 0.299*r*r + 0.587*g*g + 0.114*b*b )
    corner_hsp = math.sqrt( 0.299*c_r*c_r + 0.587*c_g*c_g + 0.114*c_b*c_b )
    if hsp < 30 and (corner_hsp+1)/(hsp+1) >= 1 and ((abs(2*r - b - g) < 15) or (abs(b - 2 * r) < 10 and abs(b - 2 * g) < 10)):
        return True
    return False

def isCounterTerrorist(img, x, y, w, h):
    mid_pos_x, mid_pos_y = getMiddlePosition(x,y,w,h)
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
        #print(getMiddlePosition(x,y,w,h))
        top_left_point = (x, y)
        bottom_right_point = (x + w, y + h)
        cv2.rectangle(sct_img, top_left_point, bottom_right_point, (0, 255, 0))

def getClosestRectangle(recs):
    min_rec = None
    min_dist = float('inf')
    for (x, y, w, h) in recs:
        mid_x, mid_y = getMiddlePosition(x,y,w,h)
        dist = (mid_x - CROSSHAIR_POSITION[0])*(mid_x - CROSSHAIR_POSITION[0]) + (mid_y - CROSSHAIR_POSITION[1])*(mid_y - CROSSHAIR_POSITION[1])
        if dist < min_dist:
            min_rec = (x, y, w, h)
            min_dist = dist
    return [min_rec] if min_rec is not None else []

while True:
    sct_img = np.array(sct.grab(bounding_box))

    rec = model.detectMultiScale(sct_img)
    
    rec = filterRectangles(rec)

    rec = cv2.groupRectangles(np.concatenate((rec, rec)).tolist(),0,eps=0.03)[0]

    rec = getClosestRectangle(rec)

    drawRectangles(rec, sct_img)

    #cv2.circle(sct_img, CROSSHAIR_POSITION, 10, (255,0,0), thickness=2)
    
    cv2.imshow('screen', sct_img)
    cur_time = time()
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
