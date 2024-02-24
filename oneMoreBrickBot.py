import pyautogui
import time

def get_window_position():
    window = pyautogui.getWindowsWithTitle("One More Brick")

    if len(window) > 0:
        window = window[0]

        window_position = window.left + 8, window.top + 1, window.right - 8, window.bottom - 9
        return window_position
    else:
        return None

def get_ball_position(window_position):

    screenshot_region = window_position[0], window_position[1] + 829, 506, 1
    screenshot = pyautogui.screenshot(region=(screenshot_region))

    width = 506

    for x in range(width):
        pixel_color = screenshot.getpixel((x, 0))

        if pixel_color == (242, 242, 242):
            return x + 12, 829 

    return None, None

def check_game_over(window_position):
    screenshot_region = window_position[0], window_position[1] + 829, 506, 1
    screenshot = pyautogui.screenshot(region=(screenshot_region))

    width = 506

    for x in range(width):
        pixel_color = screenshot.getpixel((x, 0))

        if pixel_color == (231, 64, 64):
            return False

    return True

def main():
    window_position = get_window_position()
    
    if window_position[2] - window_position[0] != 506 or window_position[3] - window_position[1] != 929:
        print("Das Fenster hat die falsche Größe!")
        return 0

    ball_x, ball_y = get_ball_position(window_position)

    if ball_x is not None and ball_y is not None:
        print("Ball bei ({}, {})".format(ball_x, ball_y))
        if ball_x < 506 / 2:
            pyautogui.moveTo(486 + window_position[0], ball_y + window_position[1])
            pyautogui.click()
        else:
            pyautogui.moveTo(20 + window_position[0], ball_y + window_position[1])
            pyautogui.click()
        return 1
    else:
        print("Keinen Ball gefunden.")
        if check_game_over(window_position):
            print("Game Over")
            pyautogui.moveTo(pyautogui.moveTo(20 + window_position[0], 50 + window_position[1]))
            pyautogui.click()
            time.sleep(5)
            pyautogui.moveTo(pyautogui.moveTo(250 + window_position[0], 450 + window_position[1]))
            print("Erneut Starten")
            pyautogui.click()
        else:
            print("Warten bis der Ball unten ankommt.")

if __name__ == "__main__":
    repeat = 1
    while(repeat):
        repeat = main()
        time.sleep(2)
