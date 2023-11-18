import joblib
import streamlit as st
from UDFs import TextPreprocessor

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
            This app uses a machine learning classifier to predict if your text is humorous or not.  
            You have the possibility to choose between two classifiers:  
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

# Preprocess user input, vectorize, and predict humor using Logistic Regression with CountVectorizer
if user_classifier == 'Logistic Regression with Stochastic Gradient Descent'\
      and user_vectorizer == 'Count Vectorizer'\
            and user_text_input:
      
      try:
            # Preprocess and vectorize user input text
            text_preprocessor = TextPreprocessor()
            preprocessed_user_text = count_vectorizer.transform([text_preprocessor.preprocess(user_text_input)])
            
            # Perform classification
            humor_prediction = lr_classifier_count_vectorized.predict(preprocessed_user_text)
            humor_probability = lr_classifier_count_vectorized.predict_proba(preprocessed_user_text)
            
            # Display classification result
            result_message = 'Your text is humorous.' if humor_prediction[0] == 1 else 'Your text is unhumorous.'
            st.write(result_message)

            # Display probability of being humorous
            st.write(f'Probability of being humorous: {humor_probability[0][1]:.2f}')
            
      except Exception as e:
            
            # Handle errors
            st.error(f"An error occurred during classification: {e}")

# Preprocess user input, vectorize, and predict humor using Logistic Regression with TF-IDF Vectorizer
if user_classifier == 'Logistic Regression with Stochastic Gradient Descent'\
      and user_vectorizer == 'TF-IDF Vectorizer'\
            and user_text_input:
      
      try:
            # Preprocess and vectorize user input text
            text_preprocessor = TextPreprocessor()
            preprocessed_user_text = tfidf_vectorizer.transform([text_preprocessor.preprocess(user_text_input)])
            
            # Perform classification
            humor_prediction = lr_classifier_tfidf_vectorized.predict(preprocessed_user_text)
            humor_probability = lr_classifier_tfidf_vectorized.predict_proba(preprocessed_user_text)
            
            # Display classification result
            result_message = 'Your text is humorous.' if humor_prediction[0] == 1 else 'Your text is unhumorous.'
            st.write(result_message)

            # Display probability of being humorous
            st.write(f'Probability of being humorous: {humor_probability[0][1]:.2f}')
            
      except Exception as e:
            
            # Handle errors
            st.error(f"An error occurred during classification: {e}")

# Preprocess user input, vectorize, and predict humor using Multinomial Naive Bayes with CountVectorizer
if user_classifier == 'Multinomial Naive Bayes'\
      and user_vectorizer == 'Count Vectorizer'\
            and user_text_input:
      
      try:
            # Preprocess and vectorize user input text
            text_preprocessor = TextPreprocessor()
            preprocessed_user_text = count_vectorizer.transform([text_preprocessor.preprocess(user_text_input)])
            
            # Perform classification
            humor_prediction = mnb_classifier_count_vectorized.predict(preprocessed_user_text)
            humor_probability = mnb_classifier_count_vectorized.predict_proba(preprocessed_user_text)
            
            # Display classification result
            result_message = 'Your text is humorous.' if humor_prediction[0] == 1 else 'Your text is unhumorous.'
            st.write(result_message)

            # Display probability of being humorous
            st.write(f'Probability of being humorous: {humor_probability[0][1]:.2f}')
            
      except Exception as e:
            
            # Handle errors
            st.error(f"An error occurred during classification: {e}")

# Preprocess user input, vectorize, and predict humor using Multinomial Naive Bayes Vectorizer
if user_classifier == 'Multinomial Naive Bayes'\
      and user_vectorizer == 'TF-IDF Vectorizer'\
            and user_text_input:
      
      try:
            # Preprocess and vectorize user input text
            text_preprocessor = TextPreprocessor()
            preprocessed_user_text = tfidf_vectorizer.transform([text_preprocessor.preprocess(user_text_input)])
            
            # Perform classification
            humor_prediction = mnb_classifier_tfidf_vectorized.predict(preprocessed_user_text)
            humor_probability = mnb_classifier_tfidf_vectorized.predict_proba(preprocessed_user_text)
            
            # Display classification result
            result_message = 'Your text is humorous.' if humor_prediction[0] == 1 else 'Your text is unhumorous.'
            st.write(result_message)

            # Display probability of being humorous
            st.write(f'Probability of being humorous: {humor_probability[0][1]:.2f}')
            
      except Exception as e:
            
            # Handle errors
            st.error(f"An error occurred during classification: {e}")

# Sample texts for reference
st.markdown('''
            Sample texts:  
            (H) Why don't Calculus majors throw house parties? Because you should never drink and derive.   
            (H) What did the shark say when he ate the clownfish? This tastes a little funny.  
            (NH) There were some heated exchanges on Ukraine and China, but strict moderation limited direct clashes.  
            (NH) Brazilian authorities made two arrests and carried out raids in key cities including Sao Paulo and Brasilia.
            '''
            )