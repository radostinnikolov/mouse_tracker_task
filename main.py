import threading

from database_writer.database_writer import DatabaseWriter
from backend import backend

from flask import Flask, render_template, Response
import cv2

writer = DatabaseWriter()
backend(writer)

app = Flask(__name__)

def gen_frames():
    while True:
        try:
            img = cv2.imread('background-prod.png')
            ret, buffer = cv2.imencode('.png', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                    b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')  # concat frame one by one and show result
        except Exception:
            img = cv2.imread('background.png')
            ret, buffer = cv2.imencode('.png', img)
            frame = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/')
def video_feed():
    return Response(gen_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')




if __name__ =="__main__":
    t1 = threading.Thread(target=backend, args=(writer,))
    t2 = threading.Thread(target=app.run, args=())

    t1.start()
    t2.start()

    t1.join()
    t2.join()


