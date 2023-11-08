import contractions
from nltk import word_tokenize
from nltk.corpus import stopwords

# Function: expand contractions (e.g., "it's" -> "it is")
def expand_contractions(text):
    return contractions.fix(text.lower(), slang = True)

# Function: extract words from text
def extract_words(text):
    return [w for w in word_tokenize(text) if w.isalpha()]

# Function: remove 'stopwords' (e.g., "the" is deleted)
def remove_stopwords(list_of_words):
    return [w for w in list_of_words if w not in stopwords.words('english')]

# Function: preprocess a list of texts
def preprocess_a_list_of_texts(list_of_texts):
    list_of_lists_of_words = [remove_stopwords(lw) for lw in [extract_words(expand_contractions(t)) for t in list_of_texts]]
    return [" ".join(list_of_lists_of_words[i]) for i in range(0, len(list_of_lists_of_words))]