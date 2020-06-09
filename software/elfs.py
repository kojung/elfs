#!/usr/bin/env python3

from flask import Flask, render_template, Response, jsonify, request
from flask_bootstrap import Bootstrap, StaticCDN
from queue import Empty, Queue
import time
import threading
import atexit
import random

from training_modes import PracticeMode, TimedMode, CountdownMode
from controller import Controller

# instantiate the app
app = Flask("ELFS")

# serve pages with bootstrap
Bootstrap(app)
app.config['BOOTSTRAP_SERVE_LOCAL'] = True

# instantiate controller
SERIAL         = '/dev/ttyUSB0'
BAUDRATE       = 9600
NUM_OF_TARGETS = 4

# singleton that keeps track of shared state
state = {
    # inter thread queue
    'queue': Queue(),

    # controller
    'controller': Controller(SERIAL, BAUDRATE),

    # current training mode
    'mode': 'practice',

    # gui states
    'gui': {
        'target': [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)],  # target states
        'total_score': 0, # total score to display
    },
}

# instantiate training modes with shared state
training = {
    'practice':  PracticeMode(state),
    'timed':     TimedMode(state),
    'countdown': CountdownMode(state)
}

# start controller thread
reader_tid = threading.Thread(target=state['controller'].reader, args=[state['queue']])
reader_tid.start()

def shutdown():
    """shutdown app gracefully"""
    # terminate the controller thread
    ctrl = state['controller']
    ctrl.terminate = True
    reader_tid.join()
    for i in range(NUM_OF_TARGETS):
        ctrl.set_target(i, "DISABLED")
    print("INFO: Controller shutdown")
    
def process_queue(state):
    """pop data from queue and perform necessary state updates"""
    cmd = state['queue'].get()
    training[state['mode']].process(cmd)

@app.route('/sse')
def sse():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            process_queue(state)
            gui = state['gui']
            cmd = """
data: { "total_score": %d, "target": %s }


""" % (gui['total_score'], str(gui['target']).replace("'", '"'))
            yield cmd
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/')
def index():
    # initialize GUI states
    gui                = state['gui']
    gui['target']      = [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)]
    gui['total_score'] = 0

    # stop all training
    for t in training.values():
        t.stop()

    return render_template('index.html')

@app.route('/stop', methods=['GET'])
def stop():
    elased_time = request.args.get('elapsedTime')
    training[state['mode']].stop()
    return jsonify(result=f"mode={state['mode']}, elased_time={elased_time}")

@app.route('/start', methods=['GET'])
def start():
    mode = request.args.get('mode')
    state['mode'] = request.args.get('mode')

    # refresh mode
    refresh_mode = request.args.get('refreshMode')

    # get mode dependent arguments
    if mode == "countdown":
        # get countdown speed
        # @TODO
        training[state['mode']].start(refresh_mode)
    else:
        training[state['mode']].start(refresh_mode)

    return jsonify(result=f"mode={state['mode']}")

def test_thread(state):
    queue = state['queue']
    time.sleep(5)
    print("Started test thread!!!")
    while True:
        # shoot a random target that is enabled in the GUI
        targets = state['gui']['target']
        enabled_targets_with_index = [(idx,target) for idx,target in enumerate(targets) if target['color'] == 'green']
        if len(enabled_targets_with_index) > 0:
            random_idx, random_target = random.choice(enabled_targets_with_index)
            queue.put(f"RSP_HIT_STATUS {random_idx} 1")
            time.sleep(2)

test_tid = threading.Thread(target=test_thread, args=[state])
test_tid.start()

atexit.register(shutdown)
app.run()
