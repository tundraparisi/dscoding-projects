# Humor Detection Project

## Overview

The Humor Detection Project aims to predict whether a given text is humorous or not using machine learning techniques. The project includes data loading, preprocessing, vectorization, model training, and a Streamlit web application for user interaction.

## Data

The project utilizes a dataset with 200,000 observations, each containing a text sample and a flag indicating whether the text is humorous or not.

## Project Structure

The project is structured as follows:

- **main.py**: Script for loading and preprocessing data, vectorizing text using Count Vectorizer and TF-IDF Vectorizer, training and evaluating two machine learning models (Multinomial Naive Bayes and Logistic Regression with Stochastic Gradient Descent), and saving the trained vectorizers and models.

- **main-jupyter.ipynb**: Jupyter Notebook version of `main.py`.

- **UDFs.py**: Script containing two classes for text preprocessing and classification. 
  - `TextPreprocessor`: Class for cleaning and preprocessing text data.
  - `TextClassifier`: Class for text classification using pre-trained models.

- **app.py**: Script for the Streamlit web application. Users can input a text, choose a classifier and vectorizer, and the app predicts whether the text is humorous or not.

## Usage

1. **Clone the Repository**
   ```bash
   git clone https://github.com/your-username/humor-detection.git
   cd humor-detection

2. **Install Dependencies**
   ```bash
   pip install -r requirements.txt

2. **Run the App**
   ```bash
   streamlit run app.py

## Humor Detection App

The Humor Detection App allows users to interactively predict the humor in a given text. Users can choose between different classifiers (Logistic Regression or Multinomial Naive Bayes) and vectorizers (Count Vectorizer or TF-IDF Vectorizer). The app leverages machine learning models trained on a dataset of 200,000 observations to provide predictions.

## Sample Texts

For reference, here are some sample texts with corresponding labels:

(H) Why don't Calculus majors throw house parties? Because you should never drink and derive.
(H) What did the shark say when he ate the clownfish? This tastes a little funny.
(NH) There were some heated exchanges on Ukraine and China, but strict moderation limited direct clashes.
(NH) Brazilian authorities made two arrests and carried out raids in key cities, including Sao Paulo and Brasilia.

Feel free to explore the app and experiment with different texts and configurations!