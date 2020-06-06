#!/usr/bin/env python3

from flask import Flask, render_template, Response, jsonify, request
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
    # GUI states
    'target': [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)],  # target states
    'timer': 0,           # time value to display
    'total_score': 0,     # total score to display
    # thread shared states
    'queue': Queue(),
    'timer_limit': -1,    # timer thread counts up to this limit and stops
    'pause_timer': True,  # pause timer
    'end_timer': False,   # terminate timer_thread
}

# start controller thread
reader_tid = threading.Thread(target=ctrl.reader, args=[state['queue']])
reader_tid.start()

# start timer thread
def timer_thread(state):
    timer = 0
    queue = state['queue']
    while not state['end_timer']:
        while not state['end_timer'] and not state['pause_timer'] and timer != state['timer_limit']:
            time.sleep(1)
            timer += 1
            queue.put(f"TIMER {timer}")

timer_tid = threading.Thread(target=timer_thread, args=[state])
timer_tid.start()   

def shutdown_controller():
    # """shutdown the controller gracefully"""
    ctrl.terminate = True
    reader_tid.join()
    for i in range(NUM_OF_TARGETS):
        ctrl.set_target(i, "DISABLED")
    print("INFO: Controller shutdown")

    state['end_timer'] = True
    timer_tid.join()
    print("INFO: Timer shutdown")
    
def process_queue(state):
    """this could be any function that blocks until data is ready"""
    cmd = state['queue'].get()
    timer_cmd = re.search(r'TIMER (\d+)', cmd)
    if timer_cmd:
        state['timer'] = int(timer_cmd.group(1))

    # sample state changes
    # state['target'][1]['color'] = 'green'
    # state['total_score'] = 100

@app.route('/sse')
def sse():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            process_queue(state)
            cmd = """
data: { "timer": %d, "total_score": %d, "target": %s }


""" % (state['timer'], state['total_score'], str(state['target']).replace("'", '"'))
            yield cmd
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/')
def index():
    # initialize GUI states
    state['target']      = [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)]
    state['pause_timer'] = True
    time.sleep(1)
    state['timer']       = 0
    state['total_score'] = 0
    return render_template('index.html')

@app.route('/stop')
def stop():
    state['pause_timer'] = True
    # time.sleep(1)
    # state['timer'] = -1
    # state['timer_limit'] = 0
    # state['pause_timer'] = False
    return jsonify(result="OK")

@app.route('/start')
def start():
    state['pause_timer'] = False
    time.sleep(2)
    state['timer'] = 0
    # state['timer_limit'] = 0
    # state['pause_timer'] = False
    return jsonify(result="OK")

atexit.register(shutdown_controller)
app.run()

