import joblib
import streamlit as st
from UDFs import TextClassifier

# Load pre-trained vectorizers and classifiers
count_vectorizer = joblib.load('count_vectorizer.joblib')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')

lr_classifier_count_vectorized = joblib.load('lr_classifier_count_vectorized.joblib')
lr_classifier_tfidf_vectorized = joblib.load('lr_classifier_tfidf_vectorized.joblib')
mnb_classifier_count_vectorized = joblib.load('mnb_classifier_count_vectorized.joblib')
mnb_classifier_tfidf_vectorized = joblib.load('mnb_classifier_tfidf_vectorized.joblib')

# Styling adjustments for better appearance
st.set_page_config(page_title = 'Humor Detection App', layout = 'wide')
st.markdown("""
            <style>
            .reportview-container {margin-top: -2em;}
            #MainMenu {visibility: hidden;}
            .stDeployButton {display:none;}
            footer {visibility: hidden;}
            #stDecoration {display:none;}
            </style>
            """,
            unsafe_allow_html = True)

# App title and description
st.title('Humor Detection App')
st.markdown('''
            This app uses machine learning classifiers to predict if your text is humorous or not.  
            You can choose between two classifiers:  
            - [Logistic Regression with Stochastic Gradient Descent](https://scikit-learn.org/stable/modules/sgd.html),  
            - [Multinomial Naive Bayes](https://scikit-learn.org/stable/modules/generated/sklearn.naive_bayes.MultinomialNB.html),
            ''')
st.markdown('''
            and two vectorizers:  
            - [Count Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.CountVectorizer.html),  
            - [TF-IDF Vectorizer](https://scikit-learn.org/stable/modules/generated/sklearn.feature_extraction.text.TfidfVectorizer.html).
            ''')
st.markdown('''
            Both classifiers and vectorizers were trained using a set of 200,000 humorous and unhumorous texts.
            ''')

# Section header for user inputs
st.header('User Inputs')

# User chooses the classifier and vectorizer
user_classifier = st.selectbox(label = 'Select classifier:',
                               index = 1,
                               options = ['Logistic Regression with Stochastic Gradient Descent',
                                          'Multinomial Naive Bayes'])
user_vectorizer = st.selectbox(label = 'Select vectorizer:',
                               index = 0,
                               options = ['Count Vectorizer',
                                          'TF-IDF Vectorizer'])

# Trained classifiers dictionary
classifiers = {
    'Logistic Regression with Stochastic Gradient Descent': {
        'Count Vectorizer': lr_classifier_count_vectorized,
        'TF-IDF Vectorizer': lr_classifier_tfidf_vectorized,
    },
    'Multinomial Naive Bayes': {
        'Count Vectorizer': mnb_classifier_count_vectorized,
        'TF-IDF Vectorizer': mnb_classifier_tfidf_vectorized,
    }
}

# Select the classifier based on user choices
selected_classifier = classifiers[user_classifier][user_vectorizer]

# Create TextClassifier instance with the selected classifier and vectorizer
classifier_instance = TextClassifier(
    selected_classifier,
    count_vectorizer if user_vectorizer == 'Count Vectorizer' else tfidf_vectorizer
)

# User enters text for classification
user_text_input = st.text_input(label = 'Enter text:')

# Section header for classification results
st.header('Classification Results')

# Placeholder to display classification results
result_placeholder = st.empty()

# Check if the user has entered text for classification
if user_text_input:
    # If yes, perform classification and display results
    classifier_instance.classify_and_display(user_text_input)
else:
    # If no text, display an informational message
    result_placeholder.info('Please select a classifier, vectorizer, and enter text for classification.')
