import re


def match_first_letters(word1, word2):
    pattern = r'^{}.*$'.format(
        re.escape(word1[:3]))  # Regex pattern to match the first three letters of word1 at the beginning of word2
    match = re.match(pattern, word2, re.IGNORECASE)

    if match:
        return True
    else:
        return False


# Example words
word1 = "Bleeding"
word2 = "BLDG"

# Check if the first three letters of the words match using regex pattern
match = match_first_letters(word1, word2)

if match:
    print("The first three letters of the words match.")
else:
    print("The first three letters of the words do not match.")
