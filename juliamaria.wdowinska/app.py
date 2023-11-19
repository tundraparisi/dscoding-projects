import joblib
import streamlit as st
from UDFs import TextClassifier

# Load the trained vectorizer and classifiers
count_vectorizer = joblib.load('count_vectorizer.joblib')
tfidf_vectorizer = joblib.load('tfidf_vectorizer.joblib')

lr_classifier_count_vectorized = joblib.load('lr_classifier_count_vectorized.joblib')
lr_classifier_tfidf_vectorized = joblib.load('lr_classifier_tfidf_vectorized.joblib')
mnb_classifier_count_vectorized = joblib.load('mnb_classifier_count_vectorized.joblib')
mnb_classifier_tfidf_vectorized = joblib.load('mnb_classifier_tfidf_vectorized.joblib')

# User input and app configuration
st.set_page_config(page_title = 'Humor Detection App', layout = 'wide')

# Styling adjustments for better appearance
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
            - Logistic Regression with Stochastic Gradient Descent,  
            - Multinomial Naive Bayes,
            ''')
st.markdown('''
            and two vectorizers:  
            - Count Vectorizer,  
            - TF-IDF Vectorizer.
            ''')
st.markdown('''
            Both the classifiers and the vectorizers were trained using a set of 200,000 humorous and unhumorous texts.
            ''')

# User chooses the classifier
user_classifier = st.selectbox(label = 'Select classifier:', index = 1,
                               options = ['Logistic Regression with Stochastic Gradient Descent',
                                          'Multinomial Naive Bayes'])

# User chooses the vectorizer
user_vectorizer = st.selectbox(label = 'Select vectorizer:', index = 0,
                               options = ['Count Vectorizer',
                                          'TF-IDF Vectorizer'])

# User enters text for classification
user_text_input = st.text_input(label = 'Enter text:')

# Create instances of TextClassifier
lr_count_classifier = TextClassifier(lr_classifier_count_vectorized, count_vectorizer)
lr_tfidf_classifier = TextClassifier(lr_classifier_tfidf_vectorized, tfidf_vectorizer)
mnb_count_classifier = TextClassifier(mnb_classifier_count_vectorized, count_vectorizer)
mnb_tfidf_classifier = TextClassifier(mnb_classifier_tfidf_vectorized, tfidf_vectorizer)

# Use instances for classification
if user_classifier == 'Logistic Regression with Stochastic Gradient Descent' and user_text_input:
    if user_vectorizer == 'Count Vectorizer':
        lr_count_classifier.classify_and_display(user_text_input)
    elif user_vectorizer == 'TF-IDF Vectorizer':
        lr_tfidf_classifier.classify_and_display(user_text_input)

elif user_classifier == 'Multinomial Naive Bayes' and user_text_input:
    if user_vectorizer == 'Count Vectorizer':
        mnb_count_classifier.classify_and_display(user_text_input)
    elif user_vectorizer == 'TF-IDF Vectorizer':
        mnb_tfidf_classifier.classify_and_display(user_text_input)

# Sample texts for reference
st.markdown('''
            Sample texts:  
            (H) Why don't Calculus majors throw house parties? Because you should never drink and derive.   
            (H) What did the shark say when he ate the clownfish? This tastes a little funny.  
            (NH) There were some heated exchanges on Ukraine and China, but strict moderation limited direct clashes.  
            (NH) Brazilian authorities made two arrests and carried out raids in key cities including Sao Paulo and Brasilia.
            '''
            )