#pip install pywhatkit
#pip install pyautogui
#pip install pynput

import pywhatkit
import pyautogui
from pynput.keyboard import Key,Controller

keyboard=Controller
x=1
h=input("when you want to sent message hours:")
m=input("minutes:")
for x in range(5):
    
    pywhatkit.sendwhatmsg('<WhatsApp_Number>', 'test 1', int(h), int(m))
    pyautogui.click()
    
    keyboard.press(Key.enter)
    keyboard.release(Key.enter)
    print("Message Send Successfully")
    tab_close=True
    
    
    m=int(m)+1