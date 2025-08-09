import ctypes
import time
from ctypes import wintypes

INPUT_MOUSE = 0
MOUSEEVENTF_MOVE = 0x0001

class MOUSEINPUT(ctypes.Structure):
    _fields_ = [("dx", wintypes.LONG),
                ("dy", wintypes.LONG),
                ("mouseData", wintypes.DWORD),
                ("dwFlags", wintypes.DWORD),
                ("time", wintypes.DWORD),
                ("dwExtraInfo", ctypes.POINTER(ctypes.c_ulong))]

class _INPUTunion(ctypes.Union):
    _fields_ = [("mi", MOUSEINPUT)]

class INPUT(ctypes.Structure):
    _anonymous_ = ("union",)
    _fields_ = [("type", wintypes.DWORD),
                ("union", _INPUTunion)]

def send_relative_mouse_move(dx, dy):
    mi = MOUSEINPUT(dx, dy, 0, MOUSEEVENTF_MOVE, 0, None)
    inp = INPUT()
    inp.type = INPUT_MOUSE
    inp.mi = mi
    ctypes.windll.user32.SendInput(1, ctypes.byref(inp), ctypes.sizeof(inp))

print("Should move in a square if it doesnt dm me!")

while True:
    send_relative_mouse_move(20, 0)   # move right
    time.sleep(0.1)
    send_relative_mouse_move(0, 20)   # move down
    time.sleep(0.1)
    send_relative_mouse_move(-20, 0)  # move left
    time.sleep(0.1)
    send_relative_mouse_move(0, -20)  # move up
    time.sleep(0.1)
