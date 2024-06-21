def calculate_metrics(true_pairs, detected_pairs):
    true_positives = len(set(true_pairs) & set(detected_pairs))
    false_positives = len(set(detected_pairs) - set(true_pairs))
    false_negatives = len(set(true_pairs) - set(detected_pairs))

    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    f_score = 2 * (precision * recall) / (precision + recall) if (precision + recall) > 0 else 0

    return precision, recall, f_score

# Manually define the detected pairs
# detected_pairs = [
#     ('CODE NOK', 'New Name 2')
# ]
detected_pairs = [
    ('RELEASE', 'New Name 0'),
    ('CODE OK', 'New Name 1'),
    ('BILLED', 'New Name 2'),
    ('DELETE', 'New Name 3'),
    ('REOPEN', 'New Name 4'),
    ('CHANGE DIAGN', 'New Name 5'),
    ('REJECT', 'New Name 6'),
    ('CHANGE END', 'New Name 7')
]




true_pairs = [
('RELEASE', 'New Name 0'),
('CODE OK', 'New Name 1'),
('BILLED', 'New Name 2'),
('DELETE', 'New Name 3'),
('REOPEN', 'New Name 4'),
('CHANGE DIAGN', 'New Name 5'),
('REJECT', 'New Name 6'),
('CHANGE END', 'New Name 7'),
('MANUAL', 'New Name 8'),
('ZDBC_BEHAN', 'New Name 9'),
('EMPTY', 'New Name 10')

]

# Calculate the metrics
precision, recall, f_score = calculate_metrics(true_pairs, detected_pairs)
print(f"Precision: {precision:.2f}")
print(f"Recall: {recall:.2f}")
print(f"F-score: {f_score:.2f}")