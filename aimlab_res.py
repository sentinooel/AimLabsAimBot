import pygetwindow as gw

windows = gw.getWindowsWithTitle('Aim Lab')

if not windows:
    print("Aim Lab window not found!")
else:
    window = windows[0]
    print(f"Aim Lab window found:")
    print(f"Left: {window.left}")
    print(f"Top: {window.top}")
    print(f"Width: {window.width}")
    print(f"Height: {window.height}")