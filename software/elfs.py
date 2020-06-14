#!/usr/bin/env python3

from flask import Flask, render_template, Response, jsonify, request
from flask_bootstrap import Bootstrap, StaticCDN
from queue import Empty, Queue
import time
import threading
import atexit
import random
import os.path
import json

from training_modes import PracticeMode, TimedMode, CountdownMode
from controller import Controller
from db import DB

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

# load default settings
rootdir = os.path.dirname(__file__)
default_cfg = os.path.join(rootdir, "default.cfg")
state['controller'].writer(default_cfg, loop=False)

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
    user         = request.args.get('user').lower()
    mode         = request.args.get('mode')
    variant      = request.args.get('variant')
    distance     = request.args.get('distance')
    total_score  = request.args.get('totalScore')
    elapsed_time = request.args.get('elapsedTime')
    db           = DB()
    db.add(user, mode, variant, distance, elapsed_time, total_score)
    training[state['mode']].stop()
    state['queue'].put("REFRESH")
    return jsonify(result="OK")

@app.route('/start', methods=['GET'])
def start():
    mode = request.args.get('mode')
    state['mode'] = request.args.get('mode')

    # refresh mode
    refresh_mode = request.args.get('refreshMode')

    # get mode dependent arguments
    if mode == "countdown":
        # get countdown speed
        speed = int(request.args.get('countdownSpeed'))
        training[state['mode']].start(refresh_mode, speed)
    else:
        training[state['mode']].start(refresh_mode)

    # push a refresh token into the queue so GUI state gets refreshed
    state['queue'].put("REFRESH")
    return jsonify(result="OK")

@app.route('/stats')
def stats():
    db = DB()
    return render_template('stats.html', db=db.db)

def refresh_thread(state):
    """Refresh state once a second, in case SSE communication fails"""
    while True:
        state['queue'].put("REFRESH")
        time.sleep(1)

refresh_tid = threading.Thread(target=refresh_thread, args=[state])
refresh_tid.start()
    
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
            coin = random.randint(0, 2)
            if coin != 0:
                queue.put(f"RSP_HIT_STATUS {random_idx} 1")
            else: # 33% chance of timeout
                queue.put(f"RSP_COUNTDOWN_EXPIRED {random_idx} 1")
            time.sleep(2)

test_tid = threading.Thread(target=test_thread, args=[state])
# test_tid.start()

atexit.register(shutdown)
app.run(host='0.0.0.0')
