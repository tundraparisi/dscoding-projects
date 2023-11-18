import joblib
import streamlit as st
from UDFs import TextPreprocessor

# Load the trained vectorizer and model
vectorizer = joblib.load('vectorizer.joblib')
mnb_classifier = joblib.load('mnb_classifier.joblib')

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
            This app uses a Multinomial Naive Bayes classifier to predict if your text is humorous or not.  
            The classifier was trained using a set of 200,000 humorous and unhumorous texts.
            '''
            )

# User enters text for classification
user_text_input = st.text_input(label = 'Enter text', value = '', placeholder = 'Enter text',
                                label_visibility = 'collapsed')

# Preprocess user input, vectorize, and predict humor using MNB classifier
if user_text_input:
      
      try:
            # Preprocess and vectorize user input text
            text_preprocessor = TextPreprocessor()
            preprocessed_user_text = vectorizer.transform([text_preprocessor.preprocess(user_text_input)])
            
            # Perform classification
            humor_prediction = mnb_classifier.predict(preprocessed_user_text)
            humor_probability = mnb_classifier.predict_proba(preprocessed_user_text)
            
            # Display classification result
            result_message = 'Your text is humorous.' if humor_prediction[0] == 1 else 'Your text is unhumorous.'
            st.write(result_message)
            
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
