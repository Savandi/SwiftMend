
import csv

def create_activity_position_mapping(event_log_file, selected_activities):
    activity_position_mapping = []
    event_counter = 0

    with open(event_log_file, 'r') as file:
        csv_reader = csv.DictReader(file)
        for row in csv_reader:
            activity = row['event']
            if activity in selected_activities:
                activity_position_mapping.append({'activity': activity, 'position': event_counter, 'event_number': len(activity_position_mapping) + 1})
            event_counter += 1

    return activity_position_mapping

def save_activity_position_mapping(activity_position_mapping, output_file):
    with open(output_file, 'w', newline='') as file:
        fieldnames = ['activity', 'position', 'event_number']
        csv_writer = csv.DictWriter(file, fieldnames=fieldnames)
        csv_writer.writeheader()
        csv_writer.writerows(activity_position_mapping)

# Example usage
event_log_file = 'data/log/Hospital billing/Hospital Billing Log.csv'
selected_activities = ['NEW', 'FIN', 'RELEASE', 'CODE OK', 'CHANGE DIAGN', 'BILLED', 'CODE ERROR', 'JOIN-PAT']
output_file = 'activity_position_mapping.csv'

activity_position_mapping = create_activity_position_mapping(event_log_file, selected_activities)
save_activity_position_mapping(activity_position_mapping, output_file)

print(f"Activity position mapping saved as {output_file}.")