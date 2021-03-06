import math

import os
import cv2
import imutils
import numpy as np
import pandas as pd

def line_detection(path_image, filename, ratio):
    """
    Detect the lines,
    take the extreme points of the lines,
    sort left extreme points radialy,
    sort left extreme points by finger,
    write coordinates to csv
    """

    # Read in image, resize, and convert to HSV colors
    img = cv2.imread(path_image)
    height, width = img.shape[:2]
    width = int((1080/height)*width)
    img = cv2.resize(img, (width, 1080), interpolation=cv2.INTER_AREA)
    hsv = cv2.cvtColor(img, cv2.COLOR_RGB2HSV)

    # Setup thresholds and apply to image, clean up contours
    lower_limit = np.array([36, 0, 0])
    upper_limit = np.array([70, 255, 255])
    threshold = cv2.inRange(hsv, lower_limit, upper_limit)
    threshold = cv2.erode(threshold, None, iterations=1)
    threshold = cv2.dilate(threshold, None, iterations=1)

    # find contours in thresholded image
    contours = cv2.findContours(threshold.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours = contours[0] if imutils.is_cv2() else contours[1]

    # TODO check if enough lines detected, else error message
    # count contours and create extremes array
    contours_count = len(contours)
    extremes = np.zeros((contours_count, 5))
    
    for c, cnts in enumerate(contours):

        # Determine the most extreme points along the contour
        extreme_left = tuple(cnts[cnts[:, :, 0].argmin()][0])
        extreme_right = tuple(cnts[cnts[:, :, 0].argmax()][0])
        # extreme_top = tuple(cnts[cnts[:, :, 1].argmin()][0])
        # extreme_bottom = tuple(cnts[cnts[:, :, 1].argmax()][0])

        # Draw each of the extreme points
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.circle(img, extreme_left, 8, (0, 0, 255), -1)
        cv2.circle(img, extreme_right, 8, (255, 0, 0), -1)
        # cv2.circle(img, extreme_top, 8, (255, 0, 0), -1)
        # cv2.circle(img, extreme_bottom, 8, (255, 255, 0), -1)

        # Store left and right extreme points
        extremes[c] = (extreme_left[0], extreme_left[1], extreme_right[0], extreme_right[1], 0)


    # Find rough middle of hand
    extremes = extremes[np.argsort(extremes[:, 0])]
    y_middle = int(extremes[0][1])
    extremes = extremes[np.argsort(extremes[:, 1])]
    x_middle = int(extremes[0][0])

    # Draw middle
    cv2.circle(img, (x_middle, y_middle), 8, (255, 0, 0), -1)

    # Calculate angle between middle and extreme points
    for e in range(0, contours_count):
        myradians = math.atan2(extremes[e][0] - y_middle, extremes[e][0] - x_middle)
        extremes[e][4] = round(myradians, 3)

    # Sort by angle, then sort by finger group
    extremes = extremes[np.argsort(extremes[:, 4])]
    # TODO Make adaptive to number of lines in image
    extremes = extremes[np.append(np.argsort(-extremes[:4, 1]), [(np.argsort(-extremes[4:10, 1]) + 4), (np.argsort(-extremes[10:16, 1]) + 10), (np.argsort(-extremes[16:22, 1]) + 16), (np.argsort(-extremes[22:28, 1]) + 22)])]

    # Draw label for extremes
    for e in range(0, contours_count):
        cv2.putText(img, str(e), (int(extremes[e, 0]), int(extremes[e, 1])), font, 0.8, (0, 0, 255))

    # Multiply extremes array by mm/pixel ratio
    extremes = extremes*ratio

    # Save coordinates arranged vertically to .csv
    extremes_df = pd.DataFrame(extremes[:,:4].reshape(contours_count*4, 1))
    extremes_df.to_csv(os.path.join(os.path.dirname(path_image), filename + ".csv"), index=False, header=False)

    # Show the output images
    # cv2.imshow('HSV', hsv)
    # cv2.imshow('threshold', threshold)
    cv2.imshow("Result", img)

    cv2.waitKey(0)
    cv2.destroyAllWindows()

# TODO remove
# line_detection('C:/Users/doorn/OneDrive/Docs/Soft-Robotics/NUS SR/Models/2D-3D_EXO/Test Images/Hand_joint-lines2.tif', 1)