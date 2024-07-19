import csv
import json
import time
import threading
from flask import Flask, Response

app = Flask(__name__)

CSV_FILE = "C:/SwiftMend/QDPES/data/demo2.csv"  # Path to your large CSV file
INTERVAL = 2 # Specify the desired interval between records in seconds

current_event = None
event_lock = threading.Lock()


def generate_event_stream():
    global current_event
    with open(CSV_FILE, "r") as file:
        csv_reader = csv.DictReader(file)
        for record in csv_reader:
            event_data = json.dumps(record)
            with event_lock:
                current_event = event_data
            time.sleep(INTERVAL)


def event_stream():
    last_event = None
    while True:
        with event_lock:
            if current_event != last_event:
                yield current_event + "\n"
                last_event = current_event
        time.sleep(INTERVAL)


@app.route("/")
def stream_events():
    return Response(event_stream(), mimetype="application/json", headers={"Transfer-Encoding": "chunked"})


if __name__ == "__main__":
    event_thread = threading.Thread(target=generate_event_stream)
    event_thread.start()
    app.run(debug=True)
