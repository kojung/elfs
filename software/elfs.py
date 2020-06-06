#!/usr/bin/env python3

from flask import Flask, render_template, Response
from flask_bootstrap import Bootstrap, StaticCDN
from queue import Empty, Queue
import time
import threading
import atexit
import re

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

# singleton that keeps track of shared state
state = {
    'queue': Queue(),
    'target': [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)],
    'timer': 0,
    'total_score': 0,
    'mode': 'practice',
    'started': False,
    'timer_limit': 20,
}

# start controller thread
reader_tid = threading.Thread(target=ctrl.reader, args=[state['queue']])
reader_tid.start()

# start timer thread
def timer_thread(state):
    timer = 0
    queue = state['queue']
    while True:
        while timer != state['timer_limit']:
            time.sleep(1)
            timer += 1
            queue.put(f"TIMER {timer}")

timer_tid = threading.Thread(target=timer_thread, args=[state])
timer_tid.start()   

def shutdown_controller():
   # """shutdown the controller gracefully"""
   print("INFO: Shutting down controller")
   ctrl.terminate = True
   reader_tid.join()
   NUM_OF_TARGETS = 4
   for i in range(NUM_OF_TARGETS):
       ctrl.set_target(i, "DISABLED")
    
def process_queue(state):
    """this could be any function that blocks until data is ready"""
    cmd = state['queue'].get()
    timer_cmd = re.search(r'TIMER (\d+)', cmd)
    if timer_cmd:
        state['timer'] = int(timer_cmd.group(1))

    return state['timer']

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/controller')
def controller():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            cmd = process_queue(state)
            yield f'data: {cmd}\n\n'
    return Response(eventStream(), mimetype="text/event-stream")

atexit.register(shutdown_controller)
app.run()

