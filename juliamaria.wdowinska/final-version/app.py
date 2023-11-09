import joblib
import streamlit as st
from UDFs import preprocess

# Load the trained vectorizer and model
vectorizer = joblib.load("vectorizer.joblib")
mnb_classifier = joblib.load("mnb_classifier.joblib")

# User-defined text (app)
st.title('Humor Detection App')

user_text = st.text_input('Enter text:')

# Preprocess 'text', vectorize and predict humor using MNB classifier
user_text1 = vectorizer.transform([preprocess(user_text)])

if st.button('Detect Humor'):
      user_prediction = mnb_classifier.predict(user_text1)
      st.write('Congratulations! This is funny.' if user_prediction[0] == 1 else 'This is not funny.')