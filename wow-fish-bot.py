from datetime import datetime
import time
import pyautogui
import numpy as np
import cv2
import sys
from PIL import ImageGrab
import subprocess
import platform


def current_timestamp():
    return datetime.now().strftime('%H:%M:%S')

if __name__ == "__main__":


    is_stop = False  # Start the bot immediately
    flag_exit = False
    lastx = 0
    lasty = 0
    is_block = False
    new_cast_time = 0
    recast_time = 40
    app = "WoW Fish BOT by YECHEZ"

    print(f"[*] {current_timestamp()} {app} started. Use Ctrl+C to stop.")
    print("[*] Focus World of Warcraft window NOW!")

    print("[*] Casting in 3...", end="", flush=True)
    time.sleep(1)
    print("2...",end="", flush=True)
    time.sleep(1)
    print("1...", flush=True)
    time.sleep(1)


    print(f"[*] {current_timestamp()} Bot started")
    while flag_exit is False:
        rect = (0, 0, 1920, 1080)  # Dummy values for the screen resolution

        if not is_block:
            lastx = 0
            lasty = 0
            pyautogui.press('1')
            print(f"[*] {current_timestamp()} Fish on!")
            new_cast_time = time.time()
            is_block = True
            time.sleep(2)
        else:
            fish_area = (0, rect[3] / 2, rect[2], rect[3])

            img = ImageGrab.grab(fish_area)
            img_np = np.array(img)

            frame = cv2.cvtColor(img_np, cv2.COLOR_BGR2RGB)
            frame_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            h_min = np.array((0, 0, 253), np.uint8)
            h_max = np.array((255, 0, 255), np.uint8)

            mask = cv2.inRange(frame_hsv, h_min, h_max)

            moments = cv2.moments(mask, 1)
            dM01 = moments['m01']
            dM10 = moments['m10']
            dArea = moments['m00']

            b_x = 0
            b_y = 0

            if dArea > 0:
                b_x = int(dM10 / dArea)
                b_y = int(dM01 / dArea)
            if lastx > 0 and lasty > 0:
                if lastx != b_x and lasty != b_y:
                    is_block = False
                    if b_x < 1: b_x = lastx
                    if b_y < 1: b_y = lasty
                    pyautogui.moveTo(b_x, b_y + fish_area[1], 0.1)
                    pyautogui.keyDown('shiftleft')
                    pyautogui.mouseDown(button='right')
                    pyautogui.mouseUp(button='right')
                    pyautogui.keyUp('shiftleft')
                    print(f"[*] {current_timestamp()} Attempting to catch")
                    time.sleep(3)
            lastx = b_x
            lasty = b_y

            if time.time() - new_cast_time > recast_time:
                print(f"[*] {current_timestamp()} New cast due to timeout.")
                is_block = False
        if cv2.waitKey(1) == 27:
            break

