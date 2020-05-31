from flask import Flask, render_template, Response
import time

app = Flask(__name__)

def get_message():
    '''this could be any function that blocks until data is ready'''
    time.sleep(1.0)
    s = time.ctime(time.time())
    print(f"Returning message {s}")
    return s

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/controller')
def controller():
    def eventStream():
        while True:
            # wait for source data to be available, then push it
            yield 'data: {}\n\n'.format(get_message())
    return Response(eventStream(), mimetype="text/event-stream")
