# import requests
# import json
# import sqlite3
# from collections import defaultdict
# import uuid
#
# # Number of events to accumulate before updating the database
# BATCH_SIZE = 2
#
# # Connect to the SQLite Database
# conn = sqlite3.connect('events.db')
# cursor = conn.cursor()
# conn.execute('''
# CREATE TABLE IF NOT EXISTS
# events (
#     case_id INTEGER,
#     event_id TEXT,
#     attributes JSON,
#     PRIMARY KEY (case_id, event_id)
# )
# ''')
# conn.commit()
# # Dictionary to store events by case ID
# case_events = defaultdict(list)
#
# STREAM_URL = "http://127.0.0.1:5000/"  # Replace with the URL of the JSON stream
# WINDOW_SIZE = 3  # Maximum number of events in the sliding window
#
#
# def subscribe_to_stream():
#     response = requests.get(STREAM_URL, stream=True)
#
#     if response.status_code == 200:
#         event_buffer = []
#         for line in response.iter_lines():
#             if line:
#                 event = line.decode("utf-8")
#                 event_buffer.append(event)
#                 event_buffer = event_buffer[-WINDOW_SIZE:]  # Truncate the list to maintain the sliding window
#                 process_event(event, event_buffer)  # logic to handle each event and sliding window
#     else:
#         print("Failed to connect to the stream. Status code:", response.status_code)
#
#
# def process_event(event, event_buffer):
#     # logic to handle each event and sliding window
#     # convert string to  object
#     event_json = json.loads(event)
#
#     case_id = int(event_json["stay_id"])
#     event_id = str(uuid.uuid4())
#
#     # Add the event to the case_events dictionary
#     case_events[case_id].append((case_id, event_id, json.dumps(event_json)))
#
#     # Check if the batch size is reached
#     if len(case_events[case_id]) >= BATCH_SIZE:
#         # Update the database with batch of events for the case
#         cursor.executemany("INSERT OR REPLACE INTO events (case_id, event_id, attributes) VALUES (?,?,?)",
#                            case_events[case_id])
#         # Clear the event batch for the case
#         case_events[case_id].clear()
#
#     if event_json["activity"] == "Triage in the ED":
#         print(event_json["chiefcomplaint"])
#     # print("Received event:", event)
#     # print("Sliding window:", event_buffer)
#     conn.commit()
#
#
# if __name__ == "__main__":
#     subscribe_to_stream()
#     conn.close()
