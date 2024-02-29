import pyautogui
import cv2
import numpy as np
import pytesseract

# function to get the current star count
def get_star_count(window_position):
    # define the screenshot region, where the star count is displayed
    screenshot_region = window_position[0] + 350, window_position[1] + 70, 150, 80
    # take the screenshot
    screenshot = pyautogui.screenshot(region=(screenshot_region))

    # convert the screenshot to NumPY-Array to pass it to OpenCV
    screenshot = np.array(screenshot)

    # create the boundries for the mask (used to mask out the star)
    lower_white = np.array([150, 150, 150])
    upper_white = np.array([255, 255, 255])

    # create the mask
    mask = cv2.inRange(screenshot, lower_white, upper_white)
    # apply the mask, we now should have an image where only the number is visible and the rest is pitch black
    processed_img = cv2.bitwise_and(screenshot, screenshot, mask= mask)
    # strecht the image on the x-axis, since the font used in One More Brick is pretty slim and tesseract has trouble recognizing it
    processed_img = cv2.resize(processed_img, None, fx= 1.7, fy= 1.0, interpolation= cv2.INTER_LINEAR)

    # get the text from the image (specify to recognize numbers)
    extracted_number = pytesseract.image_to_string(processed_img, config='--psm 6 digits')

    return extracted_number
