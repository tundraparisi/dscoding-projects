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
    
    # Expand contractions
    list_of_texts1 = []
    for t in list_of_texts:
        list_of_texts1.append(expand_contractions(t))
        
    # Extract words from text
    list_of_words1 = [extract_words(t) for t in list_of_texts1]
    
    # Remove 'stopwords'
    list_of_words2 = []
    for word in list_of_words1:
        list_of_words2.append(remove_stopwords(word))
        
    # Concatenate words back to text
    list_of_texts2 = []
    for i in range(0, len(list_of_words2)):
        list_of_texts2.append(" ".join(list_of_words2[i]))

    return list_of_texts2