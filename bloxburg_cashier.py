import pyautogui as pg
import pydirectinput as pdi
import time
import keyboard
import os
import json
from threading import Thread
from datetime import datetime

class bbimg:
    def __init__(self, key=None, action=None, pos_tuple=(), prompt_img_path="", prompt_region=(), debug=False):
        self.key=key
        self.action=action
        self.pos_tuple = pos_tuple
        self.prompt_img_path = prompt_img_path
        self.prompt_region = prompt_region
        self.debug = debug

    def locate(self, results, i):
        val = pg.locateOnScreen(self.prompt_img_path, confidence=0.9, grayscale=True, region=self.prompt_region)
        if val:
            results[i] = True
        else:
            results[i] = False
        return val

    def click(self):
        pdi.moveTo(self.pos_tuple[0], self.pos_tuple[1])
        pdi.moveTo(self.pos_tuple[0]+1, self.pos_tuple[1]+1)
        time.sleep(0.01) # Move twice for good measure - buggy
        pdi.click()

    def check(self, results, i):
        if self.locate():
            print(f"Found {self.key}!")
            self.click()
            results[i] = True
            return True
        else:
            results[i] = False
            return False

def screenshot(filename="screenshot", include_date=True, region=None):
    pic = pg.screenshot(region=region)
    now = datetime.now().strftime("%m-%d-%Y_%H-%M-%S") if include_date else ""
    path = os.path.join(os.getcwd(), "screenshots", f"{filename}_{now}.png")
    pic.save(path)

def loop_locate(objs, det_timeout=50):
    order_open = False
    no_detections = 0

    while keyboard.is_pressed('q') == False:
        # Get number of detection objects
        detect_objs = []
        for key, obj in objs.items():
            if obj.action == "detect":
                detect_objs.append(obj)

        threads = [None] * len(detect_objs)
        results = [None] * len(detect_objs)
        
        # Start threads
        for idx, obj in enumerate(detect_objs):
                threads[idx] = Thread(target=obj.locate, args=(results, idx))
                threads[idx].start()
                # print(f"Started thread {idx}")
        
        # Join threads
        for idx, obj in enumerate(detect_objs):
            threads[idx].join()
            # print(f"Joined thread {idx}")
        
        # Click on threads that found something
        for idx, obj in enumerate(detect_objs):
            if results[idx] == True:
                # print(f"{obj.key} found, clicking")
                obj.click()
                time.sleep(0.01)
                order_open = True

        if order_open:
            objs["done"].click()
            # print("clicked done!")
            order_open = False
            no_detections = 0
            time.sleep(1)

        else:
            # print("none found")
            no_detections += 1
            time.sleep(0.5)

        # Take a screenshot if something gets in the way
        if no_detections == det_timeout:
            screenshot(filename="no_detection")
            exit("Detection timed out!")


    print("Program Stopped")

def setup_objects(config, prompt_region, debug=False):
    objs = {}
    objs_dict = config["objects"]
    print("Hover over items then hit ALT\n")

    for key, obj in objs_dict.items():
        # Handle multiple types of detection?
        if obj["type"] == "button":
            # Fetch position of button
            print(obj["label"] + " - ", end="", flush=True)
            keyboard.wait(config["set_key"])
            pos = pg.position()

            objs[key] = bbimg(
                            key=key,
                            action=obj["action"],
                            pos_tuple=pos,
                            prompt_img_path=obj["detect_img_path"],
                            prompt_region=prompt_region,
                            debug=debug
                        )
            print(pos)
        

    # keyboard.wait("alt")
    # objs["b1"] = bbimg(pg.position(), 'img/b1.png', prompt_region)
    # print(pg.position())

    # print("Burger 2 - ", end="", flush=True)
    # keyboard.wait("alt")
    # objs["b2"] = bbimg(pg.position(), 'img/b2.png', prompt_region)
    # print(pg.position())

    # print("Burger 3 - ", end="", flush=True)
    # keyboard.wait("alt")
    # objs["b3"] = bbimg(pg.position(), 'img/b3.png', prompt_region)
    # print(pg.position())

    # print("Fries - ", end="", flush=True)
    # keyboard.wait("alt")
    # objs["fries"] = bbimg(pg.position(), 'img/f.png', prompt_region)
    # print(pg.position())

    # print("Soda - ", end="", flush=True)
    # keyboard.wait("alt")
    # objs["soda"] = bbimg(pg.position(), 'img/s.png', prompt_region)
    # print(pg.position())

    # print("Done button - ", end="", flush=True)
    # keyboard.wait("alt")
    # objs["done"] = bbimg(pg.position(), '')
    # print(pg.position())

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

def parse_json(path="config.json"):
    f = open(path)
    data = json.load(f)
    f.close()
    return data
    
