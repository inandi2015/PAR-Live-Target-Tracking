import os
import time
import pyautogui

def rise():
    filepath = "C:/Users/Warlock/Desktop/Lazarus 2/Backup.dwf3work"
    os.startfile(filepath)
    time.sleep(5)
    pyautogui.press('f5')
    time.sleep(2)
    pyautogui.press('f5')
    time.sleep(3)
    pyautogui.press('f5')

def kill():
    os.system('TASKKILL>NUL /F /IM Waveforms.exe')
    os.system('del /f CH1.txt')
    os.system('del /f CH2.txt')

def clearScrn():
    os.system('cls' if os.name=='nt' else 'clear')
