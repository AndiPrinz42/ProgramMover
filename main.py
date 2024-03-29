import pygetwindow as gw
import pywinauto
from screeninfo import get_monitors
import pystray
from pystray import MenuItem as Item, Menu
from PIL import Image

icon = None

def main():
    create_tray_icon()

def create_tray_icon():
    global icon
    windows = [window for window in gw.getAllWindows() if window.title]
    monitors = [monitor.name for monitor in get_monitors()]
    refresh_item = pystray.MenuItem("Refresh", lambda: update_icon(), default=True)
    menu = Menu(*[Item(window.title, Menu(*[Item(name.replace("\\\\.\\", ""), create_click_function(window.title, monitors.index(name) + 1)) for name in monitors])) for window in windows], *[refresh_item])
    icon = pystray.Icon("window", Image.open("icon.png"), "Program Mover", menu)
    icon.run_detached()

def update_icon():
    global icon
    if icon is not None:
        icon.stop()
    create_tray_icon()

def create_click_function(window, display):
    def click_function():
        return on_click(window, display)
    return click_function

def on_click(window, display):
    move_window_to_second_monitor(window, display)

def move_window_to_second_monitor(window_title, monitor):
    monitors = get_monitors()
    if len(monitors) < monitor:
        print(f"Error: Monitor not detected. There are only {len(monitors)} monitors.")
        return

    for window in gw.getAllWindows():
        if window_title in window.title:

            isMinimized = window.isMinimized
            if isMinimized:
                focus_to_window(window_title)

            isMaximized = window.isMaximized
            if isMaximized:
                window.restore()

            window.moveTo(monitors[monitor-1].x, monitors[monitor-1].y)

            focus_to_window(window_title)

            if isMaximized:
                window.maximize()

            if isMinimized:
                window.minimize()

            break


def focus_to_window(window_title):
    window = gw.getWindowsWithTitle(window_title)[0]
    if window.isActive == False:
        pywinauto.application.Application().connect(handle=window._hWnd).top_window().set_focus()

if __name__ == "__main__":
    main()