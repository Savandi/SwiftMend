import pandas as pd
from collections import Counter

def apply_renaming_and_export(input_file, output_file, renaming_intervals):
    # Load the input file
    df_input = pd.read_csv(input_file)

    # Initialize a column for the ground truth label
    df_input['ground_truth_label'] = ''

    # Apply renaming intervals and determine the most frequent label for each interval
    for start, end, labels in renaming_intervals:
        if isinstance(labels, list):  # Checking that labels is indeed a list
            most_frequent_label = Counter(labels).most_common(1)[0][0]  # Determine the most frequent label
            mask = (df_input.index >= start) & (df_input.index <= end) & (
                        (df_input['event'] == 'REJECT') | (df_input['event'] == 'rjct')| (df_input['event'] == 'reject'))
            df_input.loc[mask, 'ground_truth_label'] = most_frequent_label
        else:
            print(f"Error: Labels are not a list for interval {start} to {end}. Received: {labels}")

    # Save the updated DataFrame to a new CSV file
    df_input['position'] = range(len(df_input))
    df_input.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")

# Define renaming intervals with explicit start and end values
renaming_intervals = [
    (0, 50000, ['REJECT']),

    (50000, 100000, ['rjct','REJECT', 'REJECT', 'REJECT']),

    (100000, 150000, ['rjct', 'rjct', 'REJECT', 'REJECT', 'REJECT']),

    (150000, 200000, ['REJECT', 'reject', 'rjct', 'rjct', 'rjct']),

    (200000, 250000, ['reject', 'reject', 'rjct', 'rjct', 'rjct',]),

    (250000, 300000, ['reject']),

    (300000, 300300, ['REJECT', 'REJECT','reject','reject','reject','reject','reject','reject','reject','reject']),

    (300300, 300600, ['rjct', 'rjct','reject','reject','reject','reject','reject','reject','reject','reject']),

    (300600, 451359, ['reject'])
]

# Specify input and output file paths
input_file_path = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing_modified_REJECT_sections4.csv'
output_file_path = 'C:/Git/SwiftMend/Stream_App/REJECT_ground_truth_output_onlyREJECT_sections4.csv'

# Execute the function
apply_renaming_and_export(input_file_path, output_file_path, renaming_intervals)