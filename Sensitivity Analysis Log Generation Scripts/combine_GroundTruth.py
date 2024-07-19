import pandas as pd


def merge_and_update_labels(main_csv, ground_truth_files):
    # Load the main events CSV
    events_df = pd.read_csv(main_csv)

    # Assume the DataFrame index is equivalent to the position for the purpose of updating
    events_df.reset_index(inplace=True)
    events_df.rename(columns={'index': 'position'}, inplace=True)

    # Loop through each ground truth file and update the event labels accordingly
    for gt_file in ground_truth_files:
        # Load the ground truth data
        gt_df = pd.read_csv(gt_file)

        # Check if 'position' column exists in the ground truth DataFrame
        if 'position' not in gt_df.columns:
            raise ValueError(f"The ground truth file {gt_file} does not contain a 'position' column.")

        # Rename the column in ground truth file to 'new_event_label' to avoid confusion
        gt_df.rename(columns={'ground_truth_label': 'new_event_label'}, inplace=True)

        # Merge the ground truth labels into the main events dataframe based on the position
        events_df = pd.merge(events_df, gt_df[['position', 'new_event_label']], on='position', how='left')

        # Update the event labels where a new label is available
        events_df['event'] = events_df.apply(
            lambda row: row['new_event_label'] if pd.notnull(row['new_event_label']) else row['event'], axis=1)

        # Drop the temporary 'new_event_label' column as it's no longer needed after the update
        events_df.drop(columns=['new_event_label'], inplace=True)

    # Save the updated DataFrame to a new CSV file
    events_df.to_csv('C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital_Billing_modified_groundTruth_onlyCHANGE DIAGN_Polluted1.csv', index=False)
    print("Updated events file has been saved to 'Hospital_Billing_modified_groundTruth.csv'.")

# List of ground truth files for each activity
ground_truth_files = [
    'C:/Git/SwiftMend/Stream_App/REJECT_ground_truth_output_onlyCHANGE DIAGN_Polluted1.csv'
]

# Path to the main events CSV file
main_csv_path = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing_modified_CHANGE DIAGN_Polluted1.csv'

# Execute the function
merge_and_update_labels(main_csv_path, ground_truth_files)
