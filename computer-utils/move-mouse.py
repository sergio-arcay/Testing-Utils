# Mover el raton mediante coordenadas fijas mediante la libreria pyautogui

import pyautogui


def move_mouse(x_finger, y_finger, screen_resolution=(1920, 1080), camera_resolution=(1280, 720)):
    x_screen = x_finger * screen_resolution[0] / camera_resolution[0]
    y_screen = y_finger * screen_resolution[1] / camera_resolution[1]
    pyautogui.moveTo(x_screen, y_screen)
    return x_screen, y_screen


x_dedo, y_dedo = 100, 200
x_pantalla, y_pantalla = move_mouse(x_dedo, y_dedo)
