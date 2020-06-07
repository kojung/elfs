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
    # inter thread queue
    'queue': Queue(),

    # gui states
    'gui': {
        'target': [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)],  # target states
        'timer': 0,           # time value to display
        'total_score': 0,     # total score to display
    },

    # timer states
    'timer': {
        'curr_value': 0,
        'stop_value': -1,
        'pause_timer': True,  # pause timer
        'end_timer': False,   # terminate timer_thread
    }
}

# start controller thread
reader_tid = threading.Thread(target=ctrl.reader, args=[state['queue']])
reader_tid.start()

# start timer thread
def timer_thread(state):
    queue = state['queue']
    timer = state['timer']
    while not timer['end_timer']:
        if timer['pause_timer'] or timer['end_timer'] or timer['curr_value'] == timer['stop_value']:
            time.sleep(0)
        else:
            time.sleep(1)
            timer['curr_value'] += 1
            queue.put(f"TIMER {timer['curr_value']}")

timer_tid = threading.Thread(target=timer_thread, args=[state])
timer_tid.start()   

def shutdown():
    """shutdown app gracefully"""
    # first, terminate the controller thread
    ctrl.terminate = True
    reader_tid.join()
    for i in range(NUM_OF_TARGETS):
        ctrl.set_target(i, "DISABLED")
    print("INFO: Controller shutdown")

    # then, terminate the timer thread
    state['timer']['end_timer'] = True
    timer_tid.join()
    print("INFO: Timer shutdown")
    
def process_queue(state):
    """this could be any function that blocks until data is ready"""
    cmd = state['queue'].get()
    gui = state['gui']
    timer_cmd = re.search(r'TIMER (\d+)', cmd)
    if timer_cmd:
        gui['timer'] = int(timer_cmd.group(1))

    # sample state changes
    # state['target'][1]['color'] = 'green'
    # state['total_score'] = 100

@app.route('/sse')
def sse():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            process_queue(state)
            gui = state['gui']
            cmd = """
data: { "timer": %d, "total_score": %d, "target": %s }


""" % (gui['timer'], gui['total_score'], str(gui['target']).replace("'", '"'))
            yield cmd
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/')
def index():
    # initialize GUI states
    state['gui']['target']      = [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)]
    state['gui']['timer']       = 0
    state['gui']['total_score'] = 0
    # initialize timer states
    state['timer']['curr_value']  = 0
    state['timer']['stop_value']  = 30
    state['timer']['pause_timer'] = True
    state['timer']['end_timer']   = False
    return render_template('index.html')

@app.route('/stop')
def stop():
    state['timer']['pause_timer'] = True
    return jsonify(result="OK")

@app.route('/start', methods=['GET'])
def start():
    mode = request.args.get('mode')
    if mode == 'practice':
        pass

    elif mode == 'timed':
        pass

    elif mode == 'countdown':
        pass
    state['timer']['pause_timer'] = False
    time.sleep(1)
    state['timer']['curr_value'] = 0
    return jsonify(result=f"OK. mode={mode}")

atexit.register(shutdown)
app.run()

