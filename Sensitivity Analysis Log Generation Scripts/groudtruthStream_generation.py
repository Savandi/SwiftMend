import pandas as pd
from collections import Counter

def apply_renaming_and_export(input_file, output_file, renaming_intervals):
    # Load the position mapping for events
    df_positions = pd.read_csv(input_file)

    # Initialize a column for the ground truth label
    df_positions['ground_truth_label'] = ''

    # Apply renaming intervals and determine the most frequent label for each interval
    for placeholder, labels, start, end, in renaming_intervals:  # Ensure proper unpacking
        if isinstance(labels, list):  # Checking that labels is indeed a list
            most_frequent_label = Counter(labels).most_common(1)[0][0]  # Determine the most frequent label
            mask = (df_positions['event_number'] >= start) & (df_positions['event_number'] <= end)
            df_positions.loc[mask, 'ground_truth_label'] = most_frequent_label
        else:
            print(f"Error: Labels are not a list for interval {start} to {end}. Received: {labels}")

    # Save the updated DataFrame to a new CSV file
    df_positions.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")

# Define renaming intervals correctly
renaming_intervals = [
    # Merge and keep merged
    ('FIN', ['FIN'], 0, 15000),
    ('FIN', ['FIN', 'Fin', 'Fin'], 15001, 30000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 111', 'fin - 111'], 30001, 40000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'fin - 222', 'fin - 222', 'fin - 222'], 40001, 55000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'Over', 'Over', 'Over', 'Over', 'Over'], 55001, 65000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'Over', 'finished', 'finished', 'finished', 'finished', 'finished',
             'finished'], 65001, 74738)
]

# Specify input and output file paths
input_file_path = 'C:/Git/SwiftMend/Stream_App/FIN_position_mapping.csv'
output_file_path = 'C:/Git/SwiftMend/Stream_App/FIN_ground_truth_output_onlyFIN_second.csv'

# Execute the function
apply_renaming_and_export(input_file_path, output_file_path, renaming_intervals)
