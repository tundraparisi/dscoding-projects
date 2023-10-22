import pandas as pd
import contractions
from nltk import word_tokenize
from nltk.corpus import stopwords

dfjokes = pd.read_csv('jokes.csv')
print(dfjokes.dtypes)
print(dfjokes.head())
print(dfjokes.shape[0])

# Function: expand contractions (e.g., "it's" -> "it is")
def expand_contractions(x):
    return contractions.fix(x, slang = True)

# Function: extract words from text
def extract_words(x):
    return [w for w in word_tokenize(x) if w.isalpha()]

# Function: remove 'stopwords' (e.g., "the" is deleted)
def remove_stopwords(x):
    return [w for w in x if w not in stopwords.words('english')]

# Expand contractions
text1 = []
for element in dfjokes.text.values:
    text1.append(expand_contractions(element))

# Extract words from text
words1 = [extract_words(element) for element in text1]

# Remove 'stopwords'
text2 = []
for element in words1:
    text2.append(remove_stopwords(element))

# Concatenate words back to text
text3 = []
for i in range(0, len(text2)):
    text3.append(" ".join(text2[i]))

# Update the dataframe
dfjokes.text = text3
print(dfjokes.head())