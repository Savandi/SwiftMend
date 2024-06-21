import pandas as pd
import glob
import os


def evaluate_accuracy(output_stream_file, ground_truth_file):
    print("accraucy calculate")
    output_df = pd.read_csv(output_stream_file, usecols=['Output Activity'])
    ground_truth_df = pd.read_csv(ground_truth_file, usecols=['Final Ground Truth'])

    print(ground_truth_df.size)
    print(output_df.size)
    if len(output_df) != len(ground_truth_df):
        return None  # Data length mismatch

    TP = (output_df['Output Activity'] == ground_truth_df['Final Ground Truth']).sum()
    total = len(output_df)

    accuracy = TP / total if total else 0
    print(accuracy)
    return accuracy


# Example usage


def process_all_files(base_path):
    counter = 0
    results = []
    #output_files = glob.glob(f"{base_path}/HospitalB_EachEvent_*.csv")
    output_files = glob.glob(f"{base_path}/HospitalB_EachEvent_451359_0_0.7_modified1.csv")

    for file in output_files:
        mod_version = file.split('_modified')[1].split('.csv')[0]
        #ground_truth_file = f"{base_path}/Hospital_Billing_modified_groundTruth_{mod_version}.csv"
        ground_truth_file = f"{base_path}/final_output_withOldNewGT.csv"
        counter += 1
        print(f"Processing: {file} against {ground_truth_file} counter {counter}")  # Logging the file processing

        # Get the list of modified activities for the current log version
        modified_activities = modified_activities_dict[mod_version]

        acc = evaluate_accuracy(file, ground_truth_file)
        if acc is not None:
            results.append({'file': os.path.basename(file), 'accuracy': acc})

    results_df = pd.DataFrame(results)
    #results_df.to_csv(f"{base_path}/results_summary_new.csv", index=False)
    results_df.to_csv(f"{base_path}/accuracyof451358newgroundtruth.csv", index=False)

# Example of a dictionary storing the modified activities for each log version

modified_activities_dict = {
    '1': [
        "NEW", "neq", "New", "neww", "start",
        "FIN", "Fin", "fin - 111", "fin - 222", "Over",
        "RELEASE", "release", "release1", "release2", "output", "Release",
        "CODE OK", "code ok", "code good",
        "BILLED", "Billed", "billed", "charged", "billedd",
        "CHANGE DIAGN", "Change Diagn 1", "Change Diagn 2", "Change Diagn 3", "Update Diagn",
        "CODE ERROR", "CODE ANOMALY", "error", "Erroor", "CodeErr",
        "JOIN-PAT", "JoinPat", "JoinP", "Group-Pat", "JOIN-PAT1"
    ],
    '2': [
        "NEW", "neq", "New", "neww", "start",
        "FIN", "Fin", "fin - 111", "fin - 222", "Over",
        "RELEASE", "release", "release1", "release2", "output", "Release",
        "CODE OK", "code ok", "code good",
        "BILLED", "Billed", "billed", "charged", "billedd",
        "CHANGE DIAGN", "Change Diagn 1", "Change Diagn 2", "Change Diagn 3", "Update Diagn",
        "CODE ERROR", "CODE ANOMALY", "error", "Erroor", "CodeErr",
        "JOIN-PAT", "JoinPat", "JoinP", "Group-Pat", "JOIN-PAT1"
    ],
    '3': [
        "NEW", "neq", "neww", "New", "start", "NEW-1",
        "FIN", "Fin", "fin - 111", "fin - 222", "Over",
        "RELEASE", "release", "release1", "release2", "output", "Release", "Disperse",
        "DELETE", "remove", "clr", "Delete", "delete1", "DEL",
        "CODE OK", "code ok", "code good", "CODE",
        "BILLED", "Billed", "billed", "charged", "billedd",
        "CHANGE DIAGN", "Change Diagn 1", "Change Diagn 2", "Change Diagn 3", "Update Diagn",
        "REJECT", "refuse", "Rejectt", "Reject", "Disapprove", "REJECT111", "REJECT222",
        "CODE ERROR", "CODE ANOMALY", "error", "Erroor", "CodeErr",
        "JOIN-PAT", "JoinPat", "JoinP", "Group-Pat", "JOIN-PAT1"
    ],
    '4': [
        "NEW", "neq", "neww", "New", "start", "NEW-1",
        "FIN", "Fin", "fin - 111", "fin - 222", "Over", "Finished",
        "RELEASE", "release", "release1", "release2", "output", "Release", "relse", "Disperse",
        "DELETE", "remove", "clr", "Delete", "delete1", "delete2", "delete++", "DEL",
        "REOPEN", "Again New", "Re-Open", "Reopn", "Reopen",
        "CODE NOK", "Code not ok", "Code Not OK", "Source not good", "code nok",
        "CODE OK", "code ok", "code good", "CODE", "Script OK", "Source Good",
        "BILLED", "Billed", "billed", "charged", "billedd", "Invoiced",
        "CHANGE DIAGN", "Change Diagn 1", "Change Diagn 2", "Change Diagn 3", "Update Diagn", "Recorrect Diagnosis",
        "REJECT", "refuse", "Rejectt", "Reject", "Disapprove", "REJECT111", "REJECT222", "Decline",
        "SET STATUS", "Post Current", "set status",
        "EMPTY", "Nothing", "empty", "EMTY", "Empty",
        "CODE ERROR", "CODE ANOMALY", "error", "Erroor", "CodeErr", "BUG",
        "JOIN-PAT", "JoinPat", "JoinP", "Group-Pat", "JOIN-PAT1", "JOIN-PAT2"
    ],
    '5': [
        "NEW", "neq", "New", "neww", "start", "NEW-1",
        "FIN", "Fin", "fin - 111", "fin - 222", "Over", "Finished",
        "RELEASE", "release", "release1", "release2", "output", "Release", "Disperse",
        "DELETE", "remove", "clr", "Delete", "delete1", "delete2", "delete++", "DEL",
        "REOPEN", "Again New", "Re-Open", "Reopn", "Reopen",
        "CODE NOK", "Code not ok", "Code Not OK", "Source not good", "code nok",
        "STORNO", "storno", "Strn", "STORNO - Store Number1", "STORNO - Store Number2",
        "CODE OK", "code ok", "code good", "CODE", "Script OK", "Source Good",
        "BILLED", "Billed", "billed", "charged", "billedd", "Invoiced",
        "CHANGE DIAGN", "Change Diagn 1", "Change Diagn 2", "Change Diagn 3", "Update Diagn", "Recorrect Diagnosis",
        "REJECT", "refuse", "Rejectt", "Reject", "Disapprove", "REJECT111", "REJECT222", "Decline",
        "SET STATUS", "Post Current", "set status",
        "EMPTY", "Nothing", "empty", "EMTY", "Empty",
        "MANUAL", "manual", "Not Auto", "Physical",
        "CODE ERROR", "CODE ANOMALY", "error", "Erroor", "CodeErr", "BUG",
        "JOIN-PAT", "JoinPat", "JoinP", "Group-Pat", "JOIN-PAT1", "JOIN-PAT2",
        "CHANGE END", "Update end", "Change End", "Change last", "CHANGE-END",
        "ZDBC_BEHAN", "ZDBC_"
    ]
}

base_path = 'C:/Git/SwiftMend/Stream_App/data/log/Hospital billing'
process_all_files(base_path)