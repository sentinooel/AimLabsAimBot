import ctypes
import time
import numpy as np
import cv2
from mss import mss
import keyboard
from ctypes import wintypes
import math

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [
        ("dx", wintypes.LONG),
        ("dy", wintypes.LONG),
        ("mouseData", wintypes.DWORD),
        ("dwFlags", wintypes.DWORD),
        ("time", wintypes.DWORD),
        ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))
    ]

class _INPUTunion(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]

class INPUT(ctypes.Structure):
    _anonymous_ = ("union",)
    _fields_ = [
        ("type", wintypes.DWORD),
        ("union", _INPUTunion)
    ]

def send_relative_mouse_move(dx, dy):
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, None)
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.mi = mi
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

def get_mouse_pos():
    pt = wintypes.POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.byref(pt))
    return pt.x, pt.y

def find_all_targets(mask, min_area=100):
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    targets = []
    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area < min_area:
            continue
        M = cv2.moments(cnt)
        if M["m00"] == 0:
            continue
        cx = int(M["m10"] / M["m00"])
        cy = int(M["m01"] / M["m00"])
        targets.append((cx, cy))
    return targets

target_hsv_lower1 = np.array([40, 70, 70])
target_hsv_upper1 = np.array([80, 255, 255])


target_hsv_lower2 = np.array([0, 0, 0])
target_hsv_upper2 = np.array([0, 0, 0])

monitor = {'left': -8, 'top': -8, 'width': 1936, 'height': 1056}

key_hold = 'shift'
key_quit = 'q'

sct = mss()

print(f"[+] Hold '{key_hold}' to activate blatant aimbot (green detection), press '{key_quit}' to quit.")

while True:
    if keyboard.is_pressed(key_quit):
        print("[*] Exiting...")
        break

    if keyboard.is_pressed(key_hold):
        img = np.array(sct.grab(monitor))
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        mask = cv2.inRange(hsv, target_hsv_lower1, target_hsv_upper1)

        targets = find_all_targets(mask)
        if not targets:
            time.sleep(0.005)
            continue

        mouse_x, mouse_y = get_mouse_pos()
        rel_mouse = (mouse_x - monitor['left'], mouse_y - monitor['top'])

        closest_target = min(targets, key=lambda t: math.hypot(t[0] - rel_mouse[0], t[1] - rel_mouse[1]))
        screen_x = monitor['left'] + closest_target[0]
        screen_y = monitor['top'] + closest_target[1]

   
        dx = screen_x - mouse_x
        dy = screen_y - mouse_y

       
        send_relative_mouse_move(dx, dy)
        time.sleep(0.005)
    else:
        time.sleep(0.01)