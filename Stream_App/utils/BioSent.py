import sent2vec
import numpy as np
from numpy.linalg import norm

model = sent2vec.Sent2vecModel()
model.load_model('/Volumes/MyPassport/BioSentVec_PubMed_MIMICIII-bigram_d700.bin')


# Function to calculate similarity between two sentences
def calculate_similarity(sentence1, sentence2):
    emb1 = model.embed_sentence(sentence1).reshape(1, -1)
    emb2 = model.embed_sentence(sentence2).reshape(1, -1)
    norm_emb1 = norm(emb1)
    norm_emb2 = norm(emb2)

    if norm_emb1 == 0 or norm_emb2 == 0:
        # Handle the case when one or both of the norms are zero
        similarity = 0.0
    else:
        similarity = np.dot(emb1, emb2.T) / (norm_emb1 * norm_emb2)

    return similarity

# Example sentences
sentence1 = "Urinary Infection"
sentence2 = "UTI"

# Calculate similarity between the two sentences
similarity = calculate_similarity(sentence1, sentence2)

# Print the similarity score
print(f"Similarity between the two sentences: {similarity}")
