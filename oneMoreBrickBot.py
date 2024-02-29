import pyautogui
import time
from stats import get_star_count # used to analyze how fast you are farming stars

# function to get the position of the game window (left, right, top and bottom position)
def get_window_position():
    # get the window
    window = pyautogui.getWindowsWithTitle("One More Brick")

    if len(window) > 0: # check if the window exists
        window = window[0] # get the first window if there are multiple

        # remove the edges from the postion, since PyAutoGUI makes the window a little bigger than it is (it counts the edges where you can resize the window)
        window_position = window.left + 8, window.top + 1, window.right - 8, window.bottom - 9
        return window_position
    else:
        return None

# function to get the position of the ball
def get_ball_position(window_position):
    # define the screenshot region, because the program only looks on the base line for the ball
    screenshot_region = window_position[0], window_position[1] + 829, 506, 1 # <- the line we are checking in is only one pixel high
    # take a screenshot of the given region
    screenshot = pyautogui.screenshot(region=(screenshot_region))

    width = 506 # define the width of the window

    # go through every pixel on the screenshot
    for x in range(width):
        # get the pixel color
        pixel_color = screenshot.getpixel((x, 0))
        # check if the pixel color matches with the ball color
        if pixel_color == (242, 242, 242):
            return x + 12, 829 # return the ball position (add 12 to the x coordinate to get the center of the ball)
    return None, None

# function to check if the game can be sped up
def get_if_can_speed_up(window_position):
    # define the screenshot region (only one pixel)
    screenshot_region = window_position[0] + 468, window_position[1] + 885, 1, 1 # <- width and height are 1
    # take the screenshot
    screenshot = pyautogui.screenshot(region=(screenshot_region))
    # get the color of the pixel
    pixel_color = screenshot.getpixel((0, 0))
    # check if its white
    return pixel_color == (242, 242, 242)

# function to check if the game was sped up, this function is also used to check if all the balls are back down
# this works because if all balls are back down the "speed up" button disappears
def get_if_sped_up(window_position):
    # define the screenshot region (only one pixel)
    screenshot_region = window_position[0] + 468, window_position[1] + 885, 1, 1 # <- width and height are 1
    # take the screenshot
    screenshot = pyautogui.screenshot(region=(screenshot_region))
    # get the color of the pixel
    pixel_color = screenshot.getpixel((0, 0))
    # check if its green
    return pixel_color == (0, 255, 0)

# function to check if the game is over (it does it by checking if one pixel in the region of the continue banner has the right color)
def check_game_over(window_position):
    # define the screenshot region
    screenshot_region = window_position[0], window_position[1] + 350, 1, 1
    # take the screenshot
    screenshot = pyautogui.screenshot(region=(screenshot_region))
    # get the color of the pixel
    pixel_color = screenshot.getpixel((0, 0))
    # check if the pixel has the right color
    return pixel_color == (76, 45, 70)

# main function
def main():
    # get the window position
    window_position = get_window_position()
    
    # return if there is no window
    if window_position == None:
        print("No window found")
        return

    # return if the window has the wrong size
    if window_position[2] - window_position[0] != 506 or window_position[3] - window_position[1] != 929:
        print("The window has the wrong size!")
        return

    # check if the game is over
    if check_game_over(window_position):
        print("Game over")
        # click on the back arrow
        pyautogui.moveTo(pyautogui.moveTo(20 + window_position[0], 50 + window_position[1]))
        pyautogui.click()
        time.sleep(3) # wait some time for the animation to play after pressing the back arrow
        print("Restarting")
        # click on the play button
        pyautogui.moveTo(pyautogui.moveTo(250 + window_position[0], 470 + window_position[1]))
        pyautogui.click()
    else:
        # check if the game can be sped up
        if get_if_can_speed_up(window_position):
            # click on the button
            pyautogui.moveTo(468 + window_position[0], 885 + window_position[1])
            pyautogui.click()
            print("Sped up the game")
        # check if the speed up symbol is still there. if yes we can be sure that not all balls are back down
        elif get_if_sped_up(window_position):
            print("Waiting for the ball to come down")
        else:
            # get the ball position
            ball_x, ball_y = get_ball_position(window_position)

            # check if the ball position was found
            if ball_x is not None and ball_y is not None:
                print("Ball at {}, {}".format(ball_x, ball_y))
                # shoot in the other direction than the ball is in
                if ball_x < 506 / 2: # if the ball is on the left side
                    # shoot to the right
                    pyautogui.moveTo(486 + window_position[0], ball_y + window_position[1])
                    pyautogui.click()
                    print("Ball shot to the right")
                else: # if the ball is on the right side
                    # shoot to the left
                    pyautogui.moveTo(20 + window_position[0], ball_y + window_position[1])
                    pyautogui.click()
                    print("Ball shot to the left")
            else:
                print("Waiting for the ball to come down")

if __name__ == "__main__":
    window_position = get_window_position()
    print(get_star_count(window_position))
    #while(True): # repeat forever
        #main() # call the main function
        #time.sleep(1) # wait some time -> its not necessary repeat the main function very fast
