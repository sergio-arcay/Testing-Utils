# Mover el ratón en función de la posición del dedo índice y presentar la imagen con la deteccion en tiempo real del
# dedo en una ventana aparte.
#
# Características:
#
# - Filtro gaussiano para suavizar el movimiento del ratón
# - Presentar la imagen con la detección en tiempo real del dedo en una ventana aparte
# - Bloquear el movimiento del ratón a un punto diferente cuando no se detecte el dedo índice (no se puede usar otro medio)
# - Solo detecta una mano a la vez
# - Pulsar la tecla 'q' en la ventana de la camara para salir del programa

import mediapipe as mp
import pyautogui
import cv2


REMARK_PARAMS = 5, (0, 0, 255), -1  # radius, color, thickness
CAMERA_RESOLUTION = 640, 480
SCREEN_RESOLUTION = 1920, 1080
CAMERA = 0


def filtro_gaussiano(x, sigma):
    kernel = [1 / (1 + ((i - 2) ** 2) / (2 * sigma ** 2)) for i in range(5)]
    y = (x * kernel[0] + x * kernel[1] + x * kernel[2] + x * kernel[3] + x * kernel[4]) / 5
    return y


def move_mouse(x_finger, y_finger):
    x_new_position = x_finger * SCREEN_RESOLUTION[0] / CAMERA_RESOLUTION[0]
    y_new_position = y_finger * SCREEN_RESOLUTION[1] / CAMERA_RESOLUTION[1]

    # Obtenemos las coordenadas actuales del ratón
    x_curr_position, y_curr_position = pyautogui.position()

    # Calculamos el error entre las coordenadas del ratón y las coordenadas de la pantalla
    x_error = x_new_position - x_curr_position
    y_error = y_new_position - y_curr_position

    # Aplicamos un filtro al error para suavizar el movimiento
    x_error = filtro_gaussiano(x_error, 5)
    y_error = filtro_gaussiano(y_error, 5)

    # Movemos el ratón
    pyautogui.moveRel(x_error, y_error, 0.1)

    return x_new_position, y_new_position


def get_index_finger(frame, hand):
    # Detectamos la posición del dedo índice
    index_finger = hand.landmark[8]
    x, y = index_finger.x * frame.shape[1], index_finger.y * frame.shape[0]
    return x, y


# Inicializamos la cámara
cap = cv2.VideoCapture(CAMERA)

try:

    # Inicializamos la detección de manos
    mp_hands = mp.solutions.hands.Hands()

    # Almacemos la posición del ratón
    finger_x, finger_y = 1, 1

    # Movemos el ratón a su punto inicial
    move_mouse(finger_x, finger_y)

    import time

    # Bucle principal
    while True:

        # Capturamos una imagen de la cámara
        ret, frame = cap.read()

        # Detectamos las manos en la imagen
        results = mp_hands.process(frame)

        if results.multi_hand_landmarks:
            # Calculamos la posición del dedo índice
            finger_x, finger_y = get_index_finger(frame, results.multi_hand_landmarks[0])

        # Movemos el ratón a la posición del dedo índice
        move_mouse(finger_x, finger_y)

        # Dibujamos un círculo en la posición del dedo índice en la ventana de la cámara
        cv2.circle(frame, (int(finger_x), int(finger_y)), *REMARK_PARAMS)

        # Imprimimos el frame en la ventana de la cámara
        cv2.imshow("Hand Tracking", frame)

        # Espera a que se presione la tecla 'q' para salir del programa
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:

    # Cerramos la cámara
    cap.release()
