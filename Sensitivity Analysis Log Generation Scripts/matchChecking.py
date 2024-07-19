import pandas as pd
import glob
import os

class LogComparator:
    def __init__(self, base_path):
        self.base_path = base_path

    def compare_logs(self, output_stream_file1, output_stream_file2, ground_truth_file):
        output_df1 = pd.read_csv(output_stream_file1, usecols=['Output Activity'])
        output_df2 = pd.read_csv(output_stream_file2, usecols=['Output Activity'])
        ground_truth_df = pd.read_csv(ground_truth_file, usecols=['event'])

        if len(output_df1) != len(ground_truth_df) or len(output_df2) != len(ground_truth_df):
            return None  # Data length mismatch

        comparison_df = pd.DataFrame()
        comparison_df['Output Activity 1'] = output_df1['Output Activity']
        comparison_df['Output Activity 2'] = output_df2['Output Activity']
        comparison_df['Ground Truth'] = ground_truth_df['event']
        comparison_df['Match 1'] = output_df1['Output Activity'] == ground_truth_df['event']
        comparison_df['Match 2'] = output_df2['Output Activity'] == ground_truth_df['event']
        comparison_df.to_csv('C:/Git/SwiftMend/Stream_App/data/log/Hospital billing/comparison_result.csv', index=False)
        return comparison_df


base_path = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing'
output_stream_file1 = f"{base_path}/HospitalB_EachEvent_451_3_0.8_modified1.csv"
output_stream_file2 = f"{base_path}/HospitalB_EachEvent_225680_3_0.8_modified1.csv"
ground_truth_file = f"{base_path}/Hospital_Billing_modified_groundTruth_1.csv"

log_comparator = LogComparator(base_path)
comparison_df = log_comparator.compare_logs(output_stream_file1, output_stream_file2, ground_truth_file)
print(comparison_df)