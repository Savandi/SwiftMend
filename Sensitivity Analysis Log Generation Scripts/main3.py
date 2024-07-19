import pandas as pd

def process_csv(input_file, output_file, activities_info):
    # Read the CSV file just once
    original_df = pd.read_csv(input_file)

    # Prepare a DataFrame to hold the updated results
    modified_df = original_df.copy()

    for activity, renamed_variations, start_row, end_row in activities_info:
        # Filter for rows where the specified activity occurs each time
        activity_df = original_df[original_df['event'] == activity]

        print(f"Processing activity: {activity} from {start_row} to {end_row}")
        print(f"Total number of '{activity}' events available for processing: {len(activity_df)}")

        # Adjust the end_row if it's out of bounds
        if end_row >= len(activity_df):
            end_row = len(activity_df) - 1

        # Adjust the start_row if it's out of bounds
        if start_row >= len(activity_df):
            print(f"Start index {start_row} is out of bounds for {activity}. Skipping this activity.")
            continue

        # Rename the selected events, cycling through the variations if there are multiple
        for i, idx in enumerate(activity_df.index[start_row:end_row + 1]):
            new_activity = renamed_variations[i % len(renamed_variations)]
            modified_df.at[idx, 'event'] = new_activity

    # Export the modified DataFrame to a new CSV file
    modified_df.to_csv(output_file, index=False)
    print(f"CSV file processed. Output saved as {output_file}.")

# Define the activities to be renamed with multiple variations, including the range of events to rename
activities_info = [
    ('FIN', ['FIN', 'FIN', 'Fin'], 0, 10000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 111', 'fin - 111'], 10001, 30000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 111', 'fin - 222', 'fin - 222', 'fin - 222'], 30001, 50000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'Over', 'Over', 'Over', 'Over'], 50001, 74738)
]

input_file = 'data/log/Hospital billing/Hospital Billing Log.csv'
output_file = 'data/log/Hospital billing/Hospital Billing_modified_TESTESTTEST.csv'

process_csv(input_file, output_file, activities_info)
