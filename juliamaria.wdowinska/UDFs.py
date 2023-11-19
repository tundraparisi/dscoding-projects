import contractions
from nltk import word_tokenize, WordNetLemmatizer
from nltk.corpus import stopwords
import streamlit as st

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
    
class TextClassifier:
    """
    A class for encapsulating text classification logic using a given classifier and vectorizer.

    Parameters:
    - classifier: Machine learning classifier for text classification.
    - vectorizer: Text vectorizer to convert raw text into numerical features.

    Methods:
    - classify_and_display(user_text_input):
      Performs text classification and displays the results.

      Parameters:
      - user_text_input: The user's input text to be classified.

      Process:
      1. Preprocesses and vectorizes user input text using the specified vectorizer.
      2. Performs classification using the given classifier.
      3. Displays the classification result (humorous or unhumorous) and the probability of being humorous.

      Error Handling:
      - Catches and displays any errors that may occur during the classification process.
    """

    def __init__(self, classifier, vectorizer):
        self.classifier = classifier
        self.vectorizer = vectorizer

    # Method: classify text and display the results
    def classify_and_display(self, user_text_input):

        try:
            #  Step 1: Preprocess and vectorize user input text
            text_preprocessor = TextPreprocessor()
            preprocessed_user_text = self.vectorizer.transform([text_preprocessor.preprocess(user_text_input)])
            
            # Step 2: Perform classification
            humor_prediction = self.classifier.predict(preprocessed_user_text)
            humor_probability = self.classifier.predict_proba(preprocessed_user_text)
            
            # Step 3: Display classification result
            result_message = 'Your text is humorous.' if humor_prediction[0] == 1 else 'Your text is unhumorous.'
            st.write(result_message)

            # Step 4: Display probability of being humorous
            st.write(f'Probability of being humorous: {humor_probability[0][1]:.2f}')
        
        except Exception as e:
            # Handle errors
            st.error(f"An error occurred during classification: {e}")
