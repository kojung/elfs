#!/usr/bin/env python3

from flask import Flask, render_template, Response
from flask_bootstrap import Bootstrap, StaticCDN
import queue
import time
import threading
import atexit

from controller import Controller

app = Flask("ELFS")

# Bootstrap
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# instantiate controller
SERIAL         = '/dev/ttyUSB0'
BAUDRATE       = 9600
NUM_OF_TARGETS = 4
ctrl = Controller(SERIAL, BAUDRATE)

# use this queue to communicate with the controller
queue  = queue.Queue()
reader = threading.Thread(target=ctrl.reader, args=[queue])
reader.start()

queue.put("Hello")
queue.put("World")
for i in range(10):
    queue.put(i)

def shutdown_controller():
   # """shutdown the controller gracefully"""
   print("INFO: Shutting down controller")
   ctrl.terminate = True
   reader.join()
   NUM_OF_TARGETS = 4
   for i in range(NUM_OF_TARGETS):
       ctrl.set_target(i, "DISABLED")
    
def process_queue(queue):
    """this could be any function that blocks until data is ready"""
    cmd = queue.get()
    time.sleep(1.0)
    return cmd

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/controller')
def controller():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            cmd = process_queue(queue)
            yield f'data: {cmd}\n\n'
    return Response(eventStream(), mimetype="text/event-stream")

atexit.register(shutdown_controller)
app.run()

