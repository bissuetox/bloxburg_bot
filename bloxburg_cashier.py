import pyautogui as pg
import pydirectinput as pdi
import time
import keyboard
import win32api, win32con
import cv2 as cv
from os import getcwd

class bbimg:
    def __init__(self, pos_tuple=(), prompt_img_path="", prompt_region=()):
        self.pos_tuple = pos_tuple
        self.prompt_img_path = prompt_img_path
        self.prompt_region = prompt_region

    def locate(self):
        val = pg.locateCenterOnScreen(self.prompt_img_path, confidence=0.9, grayscale=True, region=self.prompt_region)
        # print("returning locate value {}".format(val))
        return val

    def click(self):
        # win32api.SetCursorPos(self.pos_tuple)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
        # time.sleep(0.01)
        # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)

        pdi.moveTo(self.pos_tuple[0], self.pos_tuple[1])
        time.sleep(0.05)
        pdi.click()
        time.sleep(0.05)

def screenshot(region):
    pic = pg.screenshot(region=region)
    pic.save(f"{getcwd()}\\test.png")

def loop_locate(objs):
    order_open = False
    while keyboard.is_pressed('q') == False:
        if objs["b1"].locate():
            print("found burger 1!")
            objs["b1"].click()
            order_open = True
            time.sleep(0.05)

        if objs["b2"].locate():
            print("found burger 2!")
            objs["b2"].click()
            order_open = True
            time.sleep(0.05)

        if objs["b3"].locate():
            print("found burger 3!")
            objs["b3"].click()
            order_open = True
            time.sleep(0.05)

        if objs["fries"].locate():
            print("found fries")
            objs["fries"].click()
            order_open = True
            time.sleep(0.05)

        if objs["soda"].locate():
            print("found soda")
            objs["soda"].click()
            order_open = True
            time.sleep(0.1)

        if order_open:
            time.sleep(0.5)
            objs["done"].click()
            print("clicked done!")
            order_open = False
            time.sleep(1)

        else:
            print("none found")

        time.sleep(1)

def loop_pos():
    while keyboard.is_pressed('q') == False:
        print(pg.position())
        time.sleep(0.5)

def setup_objects(prompt_region):
    objs = {}

    print("Hover over items then hit ALT\n")

    print("Burger 1 - ", end="", flush=True)
    keyboard.wait("alt")
    objs["b1"] = bbimg(pg.position(), 'img/b1.png', prompt_region)
    print(pg.position())

    print("Burger 2 - ", end="", flush=True)
    keyboard.wait("alt")
    objs["b2"] = bbimg(pg.position(), 'img/b2.png', prompt_region)
    print(pg.position())

    print("Burger 3 - ", end="", flush=True)
    keyboard.wait("alt")
    objs["b3"] = bbimg(pg.position(), 'img/b3.png', prompt_region)
    print(pg.position())

    print("Fries - ", end="", flush=True)
    keyboard.wait("alt")
    objs["fries"] = bbimg(pg.position(), 'img/f.png', prompt_region)
    print(pg.position())

    print("Soda - ", end="", flush=True)
    keyboard.wait("alt")
    objs["soda"] = bbimg(pg.position(), 'img/s.png', prompt_region)
    print(pg.position())

    print("Done button - ", end="", flush=True)
    keyboard.wait("alt")
    objs["done"] = bbimg(pg.position(), '')
    print(pg.position())

    return objs

def get_prompt_window_region():
    print("Top left of prompt area - ", end="", flush=True)
    keyboard.wait("alt")
    tl = pg.position() # Top left pos
    print(pg.position())

    print("Bottom right of prompt area - ", end="", flush=True)
    keyboard.wait("alt")
    br = pg.position() # Bottom right pos
    print(pg.position())
    width = br[0] - tl[0]
    height = br[1] - tl[1]
    print(f"W: {width}, H: {height}")
    # (left, top, width, height)
    return (tl[0], tl[1], width, height)