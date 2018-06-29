import math

import cv2
import numpy as np

button_down = False

def get_ratio(path_image):
    """
    Load and display image,
    start mouse handler,
    calculate ratio [mm/px] from line
    """

    # Load image and rescale
    img = cv2.imread(path_image, 1)
    img = cv2.resize(img, None, fx=0.4, fy=0.4, interpolation=cv2.INTER_AREA)

    # Set up data to send to mouse handler
    data = {}
    data['img'] = img.copy()

    # Set the callback function for any mouse event
    cv2.imshow("Image", img)
    cv2.setMouseCallback("Image", mouse_handler, data)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

    # Convert array to np.array in shape n,2,2
    points = np.int16(data['lines'])

    # Calculate ratio between real length and pixel length of line
    # TODO user input for real length
    real_length = 300
    pixel_length = math.sqrt(math.pow(points[0][0, 0] - points[0][1, 0], 2) + math.pow(points[0][0, 1] - points[0][1, 1], 2))
    ratio = real_length/pixel_length

    return ratio

def mouse_handler(event, x, y, flags, data):
    """
    On button down get first point,
    while button down and moving draw line,
    on button up get second point
    """

    global button_down

    if event == cv2.EVENT_LBUTTONDOWN:
        button_down = True

        data['img_copy'] = data['img'].copy()
        data['lines'] = []

        data['lines'].insert(0, [(x, y)])
        cv2.circle(data['img_copy'], (x, y), 3, (0, 0, 255), 5, 16)
        cv2.imshow("Image", data['img_copy'])

    elif event == cv2.EVENT_MOUSEMOVE and button_down:
        image = data['img_copy'].copy()
        cv2.line(image, data['lines'][0][0], (x, y), (0, 0, 0), 1)
        cv2.imshow("Image", image)

    elif event == cv2.EVENT_LBUTTONUP and button_down:
        button_down = False

        data['lines'][0].append((x, y))
        cv2.circle(data['img_copy'], (x, y), 3, (0, 0, 255), 5)
        cv2.line(data['img_copy'], data['lines'][0][0], data['lines'][0][1], (0, 0, 255), 2)
        cv2.imshow("Image", data['img_copy'])

# TODO remove
# print(get_ratio('C:/Users/doorn/OneDrive/Docs/Soft-Robotics/NUS SR/Models/2D-3D_EXO/Test Images/Hand_joint-lines2.tif'))
