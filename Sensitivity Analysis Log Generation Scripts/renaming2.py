import pandas as pd

def process_csv(input_file, output_file, section_info):
    # Read the CSV file just once
    original_df = pd.read_csv(input_file)

    # Prepare a DataFrame to hold the updated results
    modified_df = original_df.copy()

    for section_start, section_end, new_variations in section_info:
        print(f"Processing section from {section_start} to {section_end}")

        # Filter for rows within the current section
        section_df = original_df.iloc[section_start:section_end]

        # Get the indices of 'NEW' events within the section
        new_indices = section_df[section_df['event'] == 'CHANGE DIAGN'].index

        # Rename the 'NEW' events within the section based on the provided variations
        for i, idx in enumerate(new_indices):
            new_label = new_variations[i % len(new_variations)]
            modified_df.at[idx, 'event'] = new_label

    # Create a new 'position' column with incremental numbers
    modified_df['event_number'] = range(len(modified_df))

    # Export the modified DataFrame to a new CSV file
    modified_df.to_csv(output_file, index=False)
    print(f"CSV file processed. Output saved as {output_file}.")

# Define the section information and 'NEW' label variations for each section

section_info = [

    (0, 50000, ['CHANGE DIAGN']),
    (50000, 150000, ['CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN', 'CHANGE DIAGN by User1', 'CHANGE DIAGN by User3', 'CHANGE DIAGN', 'CHANGE DIAGN by User2']),
    (150000, 200000, ['CHANGE DIAGN', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN']),
    (200000, 250000, ['CHANGE DIAGN by User3', 'CHANGE DIAGN', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN by User3']),
    (250000, 300000, ['CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User1']),
    (300000, 350000, ['CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN', 'CHANGE DIAGN by User2']),
    (350000, 400000, ['CHANGE DIAGN', 'CHANGE DIAGN by User3', 'CHANGE DIAGN by User1', 'CHANGE DIAGN', 'CHANGE DIAGN by User2', 'CHANGE DIAGN', 'CHANGE DIAGN']),
    (400000, 451359, ['CHANGE DIAGN'])
]

# Example usage
input_file = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing Log.csv'
output_file = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing_modified_CHANGE DIAGN_Polluted1.csv'

process_csv(input_file, output_file, section_info)