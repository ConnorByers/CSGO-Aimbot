import numpy as np
import cv2
from mss import mss
from PIL import Image
from time import time
from pynput import keyboard

# 275 x 850
bounding_box = {'top': 150, 'left': 150, 'width': 1000, 'height': 425}

sct = mss()
sct_img = np.array(sct.grab(bounding_box))
cur_time = time()

def on_press(key):
    if key == keyboard.KeyCode.from_char('f'):
        cv2.imwrite('positive/{}.jpg'.format(cur_time), sct_img)
    elif key == keyboard.KeyCode.from_char('g'):
        cv2.imwrite('negative/{}.jpg'.format(cur_time), sct_img)

def on_release(key):
    pass


listener = keyboard.Listener(
    on_press=on_press,
    on_release=on_release)
listener.start()

while True:
    sct_img = np.array(sct.grab(bounding_box))
    sct_img = cv2.cvtColor(sct_img, cv2.COLOR_RGB2GRAY)
    cv2.imshow('screen', sct_img)
    cur_time = time()
    key = cv2.waitKey(1)
    if key == ord('q'):
        cv2.destroyAllWindows()
        break
