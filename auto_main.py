import pyautogui as pg
import time
import keyboard
# import win32api, win32con
import cv2 as cv

# for i in range(50):
#     if pg.locateOnScreen('img/burger1.png', 0.5) != None:
#         print("In view!")
#     else:
#         print("Found nothing")
#     time.sleep(0.1)

while True:
    time.sleep(0.1)
    print(pg.position())

    # x 300 - 700
    # y 430 - 900
