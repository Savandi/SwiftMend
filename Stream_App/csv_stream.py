import sys
import csv
import json
import time,os
from flask import Flask, Response, render_template, request

app = Flask(__name__)

#csv_file = "C:/SwiftMend/QDPES/data/demo3.csv"
csv_file = "C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing_modified_FIN_sections3.csv"
# csv_file = "C:/Git/SwiftMend/Stream_App/data/demo2.csv"
# csv_file = "data/demo3.csv"
#csv_file = "C:/SwiftMend/log/demo2.csv"
interval = 0.01  # Global variable for the interval between events
paused = True  # Global variable to track the paused state
next_event = False  # Global variable to track the next event request

def read_csv_and_stream(file_path):
    global paused, next_event
    with open(file_path, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            json_data = json.dumps(row)
            while paused and not next_event:
                time.sleep(0.1)  # Wait while paused and not next event
            if not paused:
                yield f"{json_data}\n"
                time.sleep(interval)  # Use the global interval variable
            elif next_event:
                next_event = False
                yield f"{json_data}\n"
                paused = True
        os._exit(0)  # Stop the stream after all events are over

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/stream')
def stream():
    return Response(read_csv_and_stream(csv_file), mimetype='application/json')

@app.route('/control', methods=['POST'])
def control():
    global paused, next_event
    action = request.form.get('action')
    if action == 'start':
        paused = False
    elif action == 'stop':
        paused = True
    elif action == 'pause':
        paused = True
    elif action == 'resume':
        paused = False
    elif action == 'next_event':
        if paused:
            next_event = True
    return "OK"

if __name__ == '__main__':
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 5000
    app.run(port=port)