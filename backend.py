import asyncio
import os
import time
import cv2
from pynput import mouse


PATH = os.getcwd()


def backend(writer):
    def on_move(x, y):
        img = cv2.imread('background.png')
        text = f"X:{x}  Y:{y}"
        coordinates = (100, 100)
        font = cv2.FONT_ITALIC
        fontScale = 1
        color = (0, 0, 0)
        thickness = 2
        output = cv2.putText(img, text, coordinates, font, fontScale, color, thickness, cv2.LINE_AA)
        cv2.imwrite('background-prod.png', output)
        asyncio.run(writer.save_data('coordinates', x, y))

    def take_picture():
        cap = cv2.VideoCapture(0)
        ret, frame = cap.read()
        if ret:
            filename = f'webcam_capture_{time.time()}.png'
            pic_path = os.path.join(PATH, filename)
            cv2.imwrite(pic_path, frame)
            asyncio.run(writer.save_data('image', pic_path))

    def on_click(x, y, button, pressed):
        if pressed and button == mouse.Button.left:
            take_picture()
        if pressed and button == mouse.Button.right:
            return False

    with mouse.Listener(
            on_move=on_move,
            on_click=on_click) as listener:
        listener.join()



# listener = mouse.Listener(
#     on_move=on_move,
#     on_click=on_click)
# listener.start()
