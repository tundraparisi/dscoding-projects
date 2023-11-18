import contractions
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords

class TextPreprocessor:
    """
    A class for preprocessing text data, including functions to expand contractions,
    extract words, remove stopwords, and lemmatize words.

    Methods:
    - expand_contractions: Expands contractions in a given text.
    - extract_words: Tokenizes and extracts alphabetic words from a given text.
    - remove_stopwords: Removes common English stopwords from a list of words.
    - lemmatize_words: Lemmatizes a list of words using WordNet.
    - preprocess: Applies the complete preprocessing pipeline to a given text.
    """

    def __init__(self):
        pass

    # Method: expand contractions (e.g., "it's" -> "it is")
    def expand_contractions(self, text):
        return contractions.fix(text.lower(), slang = True)

    # Method: extract words from text
    def extract_words(self, text):
        return [w for w in word_tokenize(text) if w.isalpha()]

    # Method: remove 'stopwords' (e.g., "the" is deleted)
    def remove_stopwords(self, list_of_words):
        return [w for w in list_of_words if w not in stopwords.words('english')]

    # Method: lemmatize words using WordNet
    def lemmatize_words(self, list_of_words):
        lemmatizer = WordNetLemmatizer()
        return [lemmatizer.lemmatize(word) for word in list_of_words]

    # Method: preprocess text
    def preprocess(self, text):
        
        # Step 1: Expand contractions
        expanded_text = self.expand_contractions(text)
        
        # Step 2: Tokenize and extract words
        words = self.extract_words(expanded_text)
        
        # Step 3: Remove stopwords
        filtered_words = self.remove_stopwords(words)
        
        # Step 4: Lemmatize words
        lemmatized_words = self.lemmatize_words(filtered_words)
        
        # Step 5: Join lemmatized words into a preprocessed text
        return " ".join(lemmatized_words)