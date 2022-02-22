import cv2 as cv
import numpy as np

if __name__ == "__main__":
    b1 = cv.imread("burger1.png", cv.IMREAD_UNCHANGED)
    b2 = cv.imread("burger2.png", cv.IMREAD_UNCHANGED)
    b3 = cv.imread("burger3.png", cv.IMREAD_UNCHANGED)
    ex = cv.imread("ex_pgm_1.png", cv.IMREAD_UNCHANGED)

    result = cv.matchTemplate(ex, b1, cv.TM_CCOEFF_NORMED)

    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(result)

    threshold = 0.5
    if max_val >= threshold:
            print("Good match!")

    cv.imshow('Result', result)
    cv.waitKey()