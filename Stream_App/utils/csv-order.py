import pandas as pd
# Read the CSV file
df = pd.read_csv('../data/mimicel.csv')
# Identify the timestamp column (assuming it's called 'timestamp')
timestamp_col = 'timestamps'
# Parse the timestamps
df[timestamp_col] = pd.to_datetime(df[timestamp_col])
# Sort the data by the timestamp column
df = df.sort_values(by=timestamp_col)
# Write the sorted data to a new CSV file
df.to_csv('output.csv', index=False)