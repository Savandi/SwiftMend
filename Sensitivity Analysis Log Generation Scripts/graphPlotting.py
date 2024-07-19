import pandas as pd
import re
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
data = pd.read_csv('data/log/Hospital billing/results_summary_new.csv')

# Function to parse the necessary details from the filename
def parse_file_details(filename):
    pattern = re.compile(r"HospitalB_EachEvent_(\d+)_(\d+)_(0\.\d+)_modified(\d+)\.csv")
    match = pattern.search(filename)
    if match:
        return {
            'window_size': int(match.group(1)),
            'delay': int(match.group(2)),
            'sim_threshold': float(match.group(3)),
            'modified_version': int(match.group(4))
        }
    return {'window_size': None, 'delay': None, 'sim_threshold': None, 'modified_version': None}

# Apply the parsing function and expand results into separate columns
details = data['file'].apply(parse_file_details)
data = pd.concat([data, pd.DataFrame(details.tolist())], axis=1)

# Function to plot graphs
def plot_modified_threshold_graphs(df, sim_thresholds, window_sizes, modified_versions):
    for modified_version in modified_versions:
        for sim_threshold in sim_thresholds:
            plt.figure(figsize=(16, 8))
            palette = sns.color_palette("husl", n_colors=df['delay'].nunique())
            for idx, delay in enumerate(sorted(df['delay'].unique())):
                mod_df = df[(df['sim_threshold'] == sim_threshold) & (df['delay'] == delay) & (df['window_size'].isin(window_sizes)) & (df['modified_version'] == modified_version)]
                sns.lineplot(data=mod_df, x='window_size', y='accuracy', marker='o', label=f'Delay {int(delay)}', color=palette[idx])
            plt.title(f'Accuracy vs Window Size for Delay Levels at Similarity Threshold {sim_threshold} (modified{modified_version})')
            plt.xlabel('Window Size')
            plt.ylabel('Accuracy')
            plt.legend(title='Delay')
            plt.grid(True)
            plt.xscale('log')  # Set the x-axis to logarithmic scale
            plt.xticks(window_sizes, labels=[str(w) for w in window_sizes], rotation=45)  # Set x-ticks and rotate for readability
            # Set y-axis to start from zero if feasible
            plt.ylim(bottom=0)
            plt.show()

# Parameters
sim_thresholds = [0.7, 0.8]
window_sizes = [226, 451, 1128, 2257, 3385, 4514, 11284, 22568, 33852, 45136, 112840, 225680, 338519, 451359]
modified_versions = [1, 2, 3, 4, 5]

# Plot
plot_modified_threshold_graphs(data, sim_thresholds, window_sizes, modified_versions)
