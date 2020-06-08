#!/usr/bin/env python3

from flask import Flask, render_template, Response, jsonify, request
from flask_bootstrap import Bootstrap, StaticCDN
from queue import Empty, Queue
import time
import threading
import atexit

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

    # timer states
    'timer': {
        'pause_timer': True,  # pause timer
        'end_timer': False,   # terminate timer_thread
        'curr_value': 0,
        'stop_value': -1,
    }
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

def timer_thread(state):
    """Time thread"""
    queue = state['queue']
    timer = state['timer']
    while not timer['end_timer']:
        if timer['pause_timer'] or timer['end_timer'] or timer['curr_value'] == timer['stop_value']:
            time.sleep(0)
        else:
            time.sleep(1)
            timer['curr_value'] += 1
            queue.put("TIMER")

timer_tid = threading.Thread(target=timer_thread, args=[state])
timer_tid.start()   

def shutdown():
    """shutdown app gracefully"""
    # terminate the controller thread
    ctrl = state['controller']
    ctrl.terminate = True
    reader_tid.join()
    for i in range(NUM_OF_TARGETS):
        ctrl.set_target(i, "DISABLED")
    print("INFO: Controller shutdown")

    # terminate the timer thread
    state['timer']['end_timer'] = True
    timer_tid.join()
    print("INFO: Timer shutdown")
    
def process_queue(state):
    """pop data from queue and perform necessary state updates"""
    cmd = state['queue'].get()
    if cmd == 'TIMER':
        # just a time event, no need to do anything
        pass
    else:
        # controller events, delegate to the training object
        training[state['mode']].process(cmd)

@app.route('/sse')
def sse():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            process_queue(state)
            gui   = state['gui']
            timer = state['timer']
            cmd = """
data: { "timer": %d, "total_score": %d, "target": %s }


""" % (timer['curr_value'], gui['total_score'], str(gui['target']).replace("'", '"'))
            yield cmd
    return Response(eventStream(), mimetype="text/event-stream")

@app.route('/')
def index():
    # initialize GUI states
    gui                = state['gui']
    gui['target']      = [{'score': 0, 'color':'lightgray'} for x in range(NUM_OF_TARGETS)]
    gui['timer']       = 0
    gui['total_score'] = 0

    # initialize timer states
    timer                = state['timer']
    timer['pause_timer'] = True
    time.sleep(1)
    timer['curr_value']  = -2
    timer['stop_value']  = 0
    timer['pause_timer'] = False
    timer['end_timer']   = False

    # stop all training
    for t in training.values():
        t.stop()

    return render_template('index.html')

@app.route('/stop')
def stop():
    training[state['mode']].stop()
    return jsonify(result=f"mode={state['mode']}, pause_timer={state['timer']['pause_timer']}")

@app.route('/start', methods=['GET'])
def start():
    state['mode'] = request.args.get('mode')
    training[state['mode']].start()
    return jsonify(result=f"mode={state['mode']}, pause_timer={state['timer']['pause_timer']}")

## def test_thread(queue):
##     time.sleep(5)
##     print("Started test thread!!!")
##     cmds = """
##         RSP_HIT_STATUS 0 1
##         RSP_HIT_STATUS 1 1
##         RSP_HIT_STATUS 2 1
##         RSP_HIT_STATUS 3 1
## """.strip().split("\n")
##     while True:
##         for cmd in cmds:
##             queue.put(cmd.strip())
##             time.sleep(2)
## 
## test_tid = threading.Thread(target=test_thread, args=[state['queue']])
## test_tid.start()

atexit.register(shutdown)
app.run()
