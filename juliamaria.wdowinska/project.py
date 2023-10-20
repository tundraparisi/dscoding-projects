import pandas as pd

dfjokes = pd.read_csv('jokes.csv')
print(dfjokes.dtypes)
print(dfjokes.head())
print(dfjokes.shape[0])

import contractions

def expand_contractions(text):
    expanded_text = contractions.fix(text, slang = True)
    return expanded_text

from nltk import word_tokenize

def extract_words(text):
    return [word for word in word_tokenize(text) if word.isalpha()]