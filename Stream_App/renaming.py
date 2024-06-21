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
    # Merge and keep merged
    ('FIN', ['FIN'], 0, 15000),
    ('FIN', ['FIN', 'Fin', 'Fin'], 15001, 30000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 111', 'fin - 111'], 30001, 40000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'fin - 222', 'fin - 222', 'fin - 222'], 40001, 55000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'Over', 'Over', 'Over', 'Over', 'Over'], 55001, 65000),
    ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'Over', 'finished', 'finished', 'finished', 'finished', 'finished', 'finished'], 65001, 74738)
#Merge and keep merged
# ('NEW', ['NEW'], 0, 10000),
# ('NEW', ['NEW', 'neq', 'neq'], 10001, 20000),
# ('NEW', ['NEW', 'neq', 'New', 'New', 'New'], 20001, 30000),
# ('NEW', ['NEW', 'neq', 'New', 'neww', 'neww', 'neww', 'neww'], 30001, 50000),
# ('NEW', ['NEW', 'neq', 'New', 'neww', 'start', 'start', 'start', 'start', 'start'], 50001, 80000),
# ('NEW', ['NEW', 'neq', 'New', 'neww', 'start', 'NEW-1','NEW-1','NEW-1','NEW-1','NEW-1','NEW-1'], 80001, 101289),
#
# ('FIN', ['FIN', 'FIN', 'Fin'], 0, 10000),
# ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 111', 'fin - 111'], 10001, 30000),
# ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 111', 'fin - 222', 'fin - 222', 'fin - 222'], 30001, 50000),
# ('FIN', ['FIN', 'Fin', 'fin - 111', 'fin - 222', 'Over', 'Over', 'Over', 'Over'], 50001, 74738),
#
# ('RELEASE', ['RELEASE', 'RELEASE', 'release'], 0, 10000),
# ('RELEASE', ['RELEASE', 'release', 'release'], 10001, 20000),
# ('RELEASE', ['RELEASE', 'release', 'release1', 'release1', 'release1'], 10001, 20000),
# ('RELEASE', ['RELEASE', 'release', 'release1', 'release2', 'release2', 'release2', 'release2'], 20001, 30000),
# ('RELEASE', ['RELEASE', 'release', 'release1', 'release2', 'output', 'output', 'output', 'output', 'output'], 30001, 40000),
# ('RELEASE', ['RELEASE', 'RELEASE', 'RELEASE', 'release', 'release1', 'release2', 'output', 'Release','Release', 'Release', 'Release'], 40001, 70926),
#
#
# #Merge and split
# ('CODE OK', ['CODE OK', 'CODE OK', 'CODE OK', 'code ok', 'code ok'], 0, 2000),
# ('CODE OK', ['CODE OK', 'code ok', 'code good', 'code good', 'code good'], 2001, 5000),
# ('CODE OK', ['CODE OK', 'code ok', 'code good', 'code OK', 'code OK', 'code OK'], 5001, 7000),
# ('CODE OK', ['CODE OK', 'code good', 'code good', 'code good'], 7001, 8000),
# ('CODE OK', ['CODE OK', 'code ok', 'code OK', 'code good', 'code good', 'code good', 'code good'], 8001, 20000),
# ('CODE OK', ['CODE OK', 'code ok', 'code OK', 'CODE OK', 'CODE OK', 'code good', 'code good'], 20001, 34003),
# #splitting starts
# ('CODE OK', ['code ok'], 36701, 36705),
# ('CODE OK', ['code OK'], 36900, 36905),
# ('CODE OK', ['code good'], 39000, 39010),
# ('CODE OK', ['code ok'], 60000, 60007),
# ('CODE OK', ['code OK'], 63000, 63008),
# ('CODE OK', ['code good'], 65000, 65008),
#
# #Merge and split
# ('BILLED', ['BILLED', 'BILLED', 'BILLED', 'Billed', 'Billed'], 0, 2000),
# ('BILLED', ['BILLED', 'Billed', 'billed', 'billed', 'billed'], 2001, 5000),
# ('BILLED', ['BILLED', 'Billed', 'billed', 'charged', 'charged', 'charged'], 5001, 7000),
# ('BILLED', ['BILLED', 'charged', 'charged', 'charged'], 7001, 8000),
# ('BILLED', ['BILLED', 'BILLED', 'BILLED', 'BILLED', 'Billed', 'billed', 'charged'], 8001, 15000),
# ('BILLED', ['BILLED', 'BILLED', 'charged', 'charged', 'Billed', 'billed', 'charged'], 15000, 20000),
# ('BILLED', ['BILLED', 'BILLED', 'Billed', 'billed'], 20001, 24000),
# ('BILLED', ['BILLED', 'BILLED', 'Billed', 'billedd', 'billed', 'billed', 'billed', 'charged'], 24001, 33724),
# #splitting starts
# ('BILLED', ['Billed', 'Billed'], 36701, 36705),
# ('BILLED', ['billed', 'billed'], 36901, 36909),
# ('BILLED', ['charged', 'charged'], 39000, 39008),
# ('BILLED', ['Billed', 'Billed'], 60000, 60004),
# ('BILLED', ['billed', 'billed'], 63000, 63007),
# ('BILLED', ['charged', 'charged'], 65000, 65009),
#
# #Merge and split
# ('CHANGE DIAGN', ['CHANGE DIAGN', 'CHANGE DIAGN', 'CHANGE DIAGN', 'Change Diagn 1', 'Change Diagn 1'], 0, 2000),
# ('CHANGE DIAGN', ['CHANGE DIAGN', 'Change Diagn 1', 'Change Diagn 2', 'Change Diagn 2', 'Change Diagn 2'], 2001, 5000),
# ('CHANGE DIAGN', ['CHANGE DIAGN', 'Change Diagn 1', 'Change Diagn 2', 'Change Diagn 3', 'Change Diagn 3', 'Change Diagn 3'], 5001, 7000),
# ('CHANGE DIAGN', ['CHANGE DIAGN', 'Update Diagn', 'Update Diagn', 'Update Diagn'], 7001, 8000),
# ('CHANGE DIAGN', ['CHANGE DIAGN', 'Change Diagn 1', 'Change Diagn 2', 'Change Diagn 3', 'Update Diagn', 'Update Diagn'], 8001, 15000),
# ('CHANGE DIAGN', ['CHANGE DIAGN', 'Change Diagn 1', 'Change Diagn 2', 'Change Diagn 3', 'Update Diagn', 'Update Diagn', 'Update Diagn'], 15000, 22724),
# #splitting starts
# ('CHANGE DIAGN', ['Change Diagn 1', 'Change Diagn 1'], 25000, 25006),
# ('CHANGE DIAGN', ['Change Diagn 2', 'Change Diagn 2'], 29000, 29009),
# ('CHANGE DIAGN', ['Change Diagn 3', 'Change Diagn 3'], 31000, 31006),
# ('CHANGE DIAGN', ['Update Diagn', 'Update Diagn'], 34000, 34004),
# ('CHANGE DIAGN', ['Change Diagn 1', 'Change Diagn 1'], 36000, 36009),
# ('CHANGE DIAGN', ['Change Diagn 2', 'Change Diagn 2'], 38000, 38009),
# ('CHANGE DIAGN', ['Change Diagn 3', 'Change Diagn 3'], 40000, 40006),
# ('CHANGE DIAGN', ['Update Diagn', 'Update Diagn'], 42000, 42005),
#
# #Not merge
# ('CODE ERROR', ['CODE ERROR', 'CODE ANOMALY', 'error', 'Erroor', 'CodeErr'], 0, 10),
# ('JOIN-PAT', ['JOIN-PAT', 'JoinPat', 'JoinP', 'Group-Pat', 'JOIN-PAT1'], 0, 10),
# ('CODE ERROR', ['CODE ERROR', 'CODE ANOMALY', 'error', 'Erroor', 'CodeErr'], 60, 70),
# ('JOIN-PAT', ['JOIN-PAT', 'JoinPat', 'JoinP', 'Group-Pat', 'JOIN-PAT1'], 300, 310),
]

# Example usage
input_file = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing Log.csv'
output_file = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/Hospital Billing_modified_onlyFIN_second.csv'


process_csv(input_file, output_file, activities_info)

