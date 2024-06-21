import pandas as pd
import random
import nltk
from nltk.corpus import wordnet

nltk.download('wordnet')
nltk.download('omw-1.4')


def get_synonyms(word):
    synonyms = set()
    for syn in wordnet.synsets(word):
        for lemma in syn.lemmas():
            synonyms.add(lemma.name())
    return list(synonyms)


def process_csv(input_file, output_file, activity_percentage, rename_percentage):
    # Read the CSV file
    df = pd.read_csv(input_file)

    # Find the number of distinct activities
    distinct_activities = df['event'].unique()
    num_distinct_activities = len(distinct_activities)
    print(f"Total number of distinct activities: {num_distinct_activities}")

    # Calculate the number of activities to select based on the percentage
    num_activities_to_select = int(num_distinct_activities * activity_percentage / 100)
    print(f"Number of selected activities: {num_activities_to_select}")

    # Randomly select the activities
    selected_activities = random.sample(list(distinct_activities), num_activities_to_select)

    # Rename events for each selected activity
    number_of_affected_activities = 0
    number_of_affected_events = 0
    renamed_activities = []

    for activity in selected_activities:
        activity_events = df[df['event'] == activity]
        num_events_to_rename = int(len(activity_events) * rename_percentage / 100)

        if num_events_to_rename >= 1:
            number_of_affected_activities += 1
            number_of_affected_events += num_events_to_rename
            events_to_rename = random.sample(list(activity_events.index), num_events_to_rename)

            # Generate different variations of the renamed activity
            activity_words = activity.split()
            renamed_variations = set()

            # Variation 1: Remove characters
            removed_chars_activity = ''.join([word[:len(word) // 2] for word in activity_words])
            renamed_variations.add(removed_chars_activity)

            # Variation 2: Use synonyms for each word
            synonym_words = []
            for word in activity_words:
                synonyms = get_synonyms(word)
                if synonyms:
                    synonym_word = random.choice(synonyms)
                    synonym_words.append(synonym_word)
                else:
                    synonym_words.append(word)
            synonym_activity = ' '.join(synonym_words)
            renamed_variations.add(synonym_activity)

            # Variation 3: Remove characters from synonyms
            removed_chars_synonym = ''.join([word[:len(word) // 2] for word in synonym_words])
            renamed_variations.add(removed_chars_synonym)

            # Randomly select a variation for each event to rename
            for event_index in events_to_rename:
                renamed_activity = random.choice(list(renamed_variations))
                df.at[event_index, 'event'] = renamed_activity

            renamed_activities.append((activity, list(renamed_variations)))

    print(f"Total number of affected activities: {number_of_affected_activities}")
    print(f"Total number of affected events: {number_of_affected_events}")

    # Export the modified CSV file
    df.to_csv(output_file, index=False)
    print(f"CSV file processed. Output saved as {output_file}.")

    # Create a ground truth text file
    ground_truth_file = output_file[:-4] + "_ground_truth.txt"
    with open(ground_truth_file, 'w') as file:
        for activity, variations in renamed_activities:
            file.write(f"{activity} = {', '.join(variations)}\n")

    print(f"Ground truth file generated: {ground_truth_file}")

    print();

    return num_distinct_activities, len(
        selected_activities), number_of_affected_activities, number_of_affected_events, renamed_activities


# Example usage
input_files = ['BPI_2017_Loan_Application Log.csv']
parameter_pairs = [(20, 0.1), (20, 10), (20, 30), (40, 30), (40, 50), (60, 50), (80, 50), (100, 50)]
num_runs = 5

results = []

for input_file in input_files:
    for activity_percentage, rename_percentage in parameter_pairs:
        for run in range(1, num_runs + 1):
            output_file = f"{input_file[:-4]}_mod_a{activity_percentage}_r{rename_percentage}_run{run}.csv"
            num_distinct_activities, selected_activities, number_of_affected_activities, num_affected_events, renamed_activities = process_csv(
                input_file, output_file, activity_percentage, rename_percentage)
            results.append((input_file, activity_percentage, rename_percentage, run, num_distinct_activities,
                            selected_activities, number_of_affected_activities, num_affected_events,
                            renamed_activities))

# Print the results
print(
    "Input File | Activity % | Rename % | Run | Distinct Activities | Selected Activities | Affected Activities | Affected Events | Renamed Activities")
for result in results:
    print(
        f"{result[0]} | {result[1]} | {result[2]} | {result[3]} | {result[4]} | {result[5]} | {result[6]} | {result[7]} | {', '.join([f'{activity}: {variations}' for activity, variations in result[8]])}")