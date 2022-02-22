import pyautogui as pg
import pydirectinput as pdi
import time
import keyboard
from datetime import datetime

class bbimg:
    def __init__(self, pos_tuple=(), prompt_img_path="", prompt_region=()):
        self.pos_tuple = pos_tuple
        self.prompt_img_path = prompt_img_path
        self.prompt_region = prompt_region

    def locate(self):
        val = pg.locateOnScreen(self.prompt_img_path, confidence=0.9, grayscale=True, region=self.prompt_region)
        return val

    def click(self):
        pdi.moveTo(self.pos_tuple[0], self.pos_tuple[1])
        time.sleep(0.05) # Move twice for good measure - buggy
        pdi.moveTo(self.pos_tuple[0]+1, self.pos_tuple[1]+1)
        pdi.click()

def screenshot(filepath="test.png", region=None):
    pic = pg.screenshot(region=region)
    pic.save(filepath)

def loop_locate(objs, det_timeout=50, debug=False):
    order_open = False
    no_detections = 0

    while keyboard.is_pressed('q') == False:
        if objs["b1"].locate():
            if debug: print("found burger 1!")
            objs["b1"].click()
            order_open = True

        if objs["b2"].locate():
            if debug: print("found burger 2!")
            objs["b2"].click()
            order_open = True

        if objs["b3"].locate():
            if debug: print("found burger 3!")
            objs["b3"].click()
            order_open = True

        if objs["fries"].locate():
            if debug: print("found fries")
            objs["fries"].click()
            order_open = True

        if objs["soda"].locate():
            if debug: print("found soda")
            objs["soda"].click()
            order_open = True

        if order_open:
            objs["done"].click()
            if debug: print("clicked done!")
            order_open = False
            no_detections = 0

        else:
            if debug: print("none found")
            no_detections += 1
            time.sleep(0.5)

        # Take a screenshot if something gets in the way
        if no_detections >= det_timeout:
            now = datetime.now().strftime("%H-%M-%S")
            screenshot(filepath=f"no_detection_{now}.png")
            exit("Detection timed out!")

    print("Program Stopped")

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