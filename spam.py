import pyautogui
import keyboard
import time


print("Spamming will start in 3 seconds")
time.sleep(1)
print("Spamming will start in 2 seconds")
time.sleep(1)
print("Spamming will start in 1 seconds")
time.sleep(1)
print("Spamming has started")



def spam():
    while True:
        # do command+v,@95246601248
        pyautogui.typewrite("<@952466012488474694>")



        
        pyautogui.press("enter")

        # check if m is pressed
        if keyboard.is_pressed('m'):
            break

        
        

spam()