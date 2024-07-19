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
                        (df_input['event'] == 'CHANGE DIAGN') | (df_input['event'] == 'CHANGE DIAGN by User1') | (df_input['event'] == 'CHANGE DIAGN by User2') | (df_input['event'] == 'CHANGE DIAGN by User3'))
            df_input.loc[mask, 'ground_truth_label'] = most_frequent_label
        else:
            print(f"Error: Labels are not a list for interval {start} to {end}. Received: {labels}")

    # Save the updated DataFrame to a new CSV file
    df_input['position'] = range(len(df_input))
    df_input.to_csv(output_file, index=False)
    print(f"Output saved to {output_file}")

# Define renaming intervals with explicit start and end values
renaming_intervals = [
    (0, 50000, ['CHANGE DIAGN']),
    (50000, 150000, ['CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN', 'CHANGE DIAGN by User1', 'CHANGE DIAGN by User3', 'CHANGE DIAGN', 'CHANGE DIAGN by User2']),
    (150000, 200000, ['CHANGE DIAGN', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN']),
    (200000, 250000, ['CHANGE DIAGN by User3', 'CHANGE DIAGN', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN by User3']),
    (250000, 300000, ['CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User1']),
    (300000, 350000, ['CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN', 'CHANGE DIAGN by User2']),
    (350000, 400000, ['CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN']),
    (400000, 451359, ['CHANGE DIAGN'])
]

# Specify input and output file paths
input_file_path = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing_modified_CHANGE DIAGN_Polluted1.csv'
output_file_path = 'C:/Git/SwiftMend/Stream_App/REJECT_ground_truth_output_onlyCHANGE DIAGN_Polluted1.csv'

# Execute the function
apply_renaming_and_export(input_file_path, output_file_path, renaming_intervals)