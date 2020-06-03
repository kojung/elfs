from flask import Flask, render_template, Response
from queue import Queue
import time

from controller import Controller

app = Flask("ELFS")

# instantiate controller
ctrl = Controller()

# use this queue to communicate with the controller
queue = Queue()

def get_message():
    '''this could be any function that blocks until data is ready'''
    time.sleep(1.0)
    s = time.ctime(time.time())
    return s

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/elfs')
def controller():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")
