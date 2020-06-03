from flask import Flask, render_template, Response
import Queue
import time
import threading
import atexit

from controller import Controller

app = Flask("ELFS")

# instantiate controller
SERIAL         = '/dev/ttyUSB0'
BAUDRATE       = 9600
NUM_OF_TARGETS = 4
ctrl = Controller(SERIAL, BAUDRATE)

# use this queue to communicate with the controller
queue  = Queue.Queue()
reader = threading.Thread(target=ctrl.reader, args=[queue])
reader.start()

def shutdown_controller():
    """shutdown the controller gracefully"""
    print("Shutting down controller")
    ctrl.terminate = True
    reader.join()
    NUM_OF_TARGETS = 4
    for i in range(NUM_OF_TARGETS):
        ctrl.set_target(i, "DISABLED")
    
def get_message():
    """this could be any function that blocks until data is ready"""
    return queue.get()
    return s

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/controller')
def controller():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")

atexit.register(xxxhutdown_controller)
