import requests
import json
from collections import defaultdict
import re
import nltk
import Levenshtein

nltk.download('wordnet')
nltk.download('omw-1.4')
nltk.download('punkt')
from nltk.corpus import wordnet

STREAM_URL = "http://127.0.0.1:5000/"  # Replace with the URL of the JSON stream
WINDOW_SIZE = 3  # Maximum number of events in the sliding window
raw_group = defaultdict(list)  # Store the chiefcomplaint value events
cleaned_group = defaultdict()
ALERT_THRESHOLD = 2
alert_group = defaultdict(list)
L_SIMILARITY_THRESHOLD = 0.75


# Method for checking if a word is actually a word or not
def is_word_in_wordnet(word):
    synsets = wordnet.synsets(word)
    if synsets:
        return True
    else:
        return False


# Getting the similarity between the cleaned words
def check_cleaned_similarity(cleaned_text):
    return_cleaned = ""
    if len(cleaned_group) != 0:
        # print(cleaned_group)
        # copy snapshot of cleaned_group key values
        # create a new dictionary with keys copied from the defaultdict
        cleaned_list = dict.fromkeys(cleaned_group.keys())
        # loop through those values and create 2d array with sim_score
        for key in cleaned_list:
            distance = Levenshtein.distance(cleaned_text.lower(), key.lower())
            max_length = max(len(cleaned_text), len(key))
            similarity = 1 - distance / max_length
            cleaned_list[key] = similarity
        # filter the values more than 75% sim\
        # print(cleaned_list)
        key_with_max_value = max(cleaned_list, key=cleaned_list.get)
        max_value = cleaned_list[key_with_max_value]
        if max_value >= L_SIMILARITY_THRESHOLD:
            return_cleaned += key_with_max_value
    return return_cleaned


def subscribe_to_stream():
    response = requests.get(STREAM_URL, stream=True)

    if response.status_code == 200:
        event_buffer = []
        for line in response.iter_lines():
            if line:
                event = line.decode("utf-8")
                event_buffer.append(event)
                event_buffer = event_buffer[-WINDOW_SIZE:]  # Truncate the list to maintain the sliding window
                process_event(event, event_buffer)  # logic to handle each event and sliding window
    else:
        print("Failed to connect to the stream. Status code:", response.status_code)


def process_event(event, event_buffer):
    # logic to handle each event and sliding window
    # convert string to  object
    event_json = json.loads(event)

    case_id = int(event_json["stay_id"])
    event_id = str(event_json["event_id"])

    if event_json["activity"] == "Triage in the ED":
        print()
        # Only Process the event when the activity name is Triage in the ED
        chief_value = event_json["chiefcomplaint"]
        print("New stream item: " + chief_value)
        # Check the value is null or not
        if chief_value != "":
            # First Save the chief_value
            # Needs to consider the special characters and null values as quality drifts as well (future work). If all special characters are cleaned then it would result in null
            # - values and would overlap will real null values
            cleaned_text = re.sub(r'[^a-zA-Z0-9\s]', '', chief_value)
            cleaned_text = cleaned_text.lower()

            # check whether for wordnet
            words = nltk.word_tokenize(cleaned_text)
            cleaned_words = [word.lower() for word in words if word.isalpha()]

            # init acronym detected variable
            acronym_found = False
            for word in cleaned_words:
                if not is_word_in_wordnet(word):
                    # Found acronym
                    acronym_found = True
            if acronym_found:
                # Acronym sentence method
                print()
            else:
                # call other method
                # check for raw_group value if no value then apply default first time values
                if chief_value in raw_group:
                    # increment the frequency and check for alerting
                    # increment frequency
                    raw = raw_group[chief_value][0]
                    temp_freq = raw_group[chief_value][0][1] + 1
                    temp_leading = raw_group[chief_value][0][2]
                    print("Temp Leading: " + str(temp_leading))
                    temp_cleaned = raw_group[chief_value][0][0]
                    temp_events = json.loads(raw_group[chief_value][0][3])

                    # update frequency
                    temp_raw = list(raw)
                    temp_raw[1] += 1

                    # update event to the event list
                    temp_events["events"].append(
                        {"event_id": event_id, "timestamp": event_json["timestamps"], "raw_value": chief_value})
                    temp_raw[3] = json.dumps(temp_events)

                    raw_group[chief_value][0] = tuple(temp_raw)

                    # update the cleaned_group
                    temp_cleaned_group = json.loads(cleaned_group[temp_cleaned])
                    temp_cleaned_group["events"].append(
                        {"event_id": event_id, "timestamp": event_json["timestamps"], "raw_value": chief_value})
                    cleaned_group[temp_cleaned] = json.dumps(temp_cleaned_group)

                    # check whether it is the leading value
                    if not temp_leading:
                        # if it is not the leading value
                        # find who is the leading and compare the new freq value with it
                        filtered_data = [item for sublist in raw_group.values() for item in sublist if
                                         item[0] == temp_cleaned]
                        frequencies = [item[1] for item in filtered_data]
                        highest_frequency = max(frequencies)

                        # Find the case with the highest frequency for the cleaned_text
                        raw_with_highest_frequency = next((case_id for case_id in raw_group.keys() if any(
                            item[1] == highest_frequency for item in raw_group[case_id] if item[0] == cleaned_text)),
                                                          None)
                        print(highest_frequency, "'" + raw_with_highest_frequency + "'" , temp_freq, "'" + chief_value + "'" )

                        # check whether can it be the leading value then change the leading value
                        if temp_freq > highest_frequency:
                            # Update new one as the leading, remove old one from the leading
                            temp_raw[2] = True
                            raw_group[chief_value][0] = tuple(temp_raw)
                            print("changed the leading from: '"+raw_with_highest_frequency+"' To: '"+chief_value+"'")
                            temp_raw_with_highest_frequency = list(raw_group[raw_with_highest_frequency][0])
                            temp_raw_with_highest_frequency[2] = False
                            raw_group[raw_with_highest_frequency][0] = tuple(temp_raw_with_highest_frequency)

                        # alert checking
                        if not raw_group[chief_value][0][2] and temp_freq > ALERT_THRESHOLD:
                            alert_group[chief_value].append((cleaned_text, raw_group[chief_value][0][3]))
                            print("Raw Value : "+str(chief_value)+" ALERT: " + str(alert_group[chief_value]))
                else:
                    # value not found on the raw_group need to add the value
                    temp_freq = 1
                    temp_events = {"events": [
                        {"event_id": event_id, "timestamp": event_json["timestamps"], "raw_value": chief_value}]}
                    temp_leading = False

                    # New item therefore need to create cleaned value for the event
                    # check item is in the cleaned_group
                    sim_cleand = check_cleaned_similarity(cleaned_text)
                    if len(sim_cleand) == 0:
                        # add new item to the cleaned group
                        # create event json
                        temp_event = '{"events": []}'
                        temp_event_json = json.loads(temp_event)
                        temp_event_json["events"].append(
                            {"event_id": event_id, "timestamp": event_json["timestamps"], "raw_value": chief_value})
                        updated_event_json = json.dumps(temp_event_json)
                        cleaned_group[cleaned_text] = updated_event_json
                        # print(cleaned_group)
                        # mark as leading
                        temp_leading = True
                        # append to raw_group
                        raw_group[chief_value].append((cleaned_text, temp_freq, temp_leading, json.dumps(temp_events)))
                        # print(raw_group)
                    else:
                        # update the cleaned group
                        print(cleaned_group[sim_cleand])
                        temp_events_json = json.loads(cleaned_group[sim_cleand])
                        temp_events_json["events"].append(
                            {"event_id": event_id, "timestamp": event_json["timestamps"], "raw_value": chief_value})
                        cleaned_group[sim_cleand] = json.dumps(temp_events_json)
                        raw_group[chief_value].append((sim_cleand, temp_freq, temp_leading, json.dumps(temp_events)))

    # print("Received event:", event)
    # print("Sliding window:", event_buffer)


if __name__ == "__main__":
    subscribe_to_stream()
