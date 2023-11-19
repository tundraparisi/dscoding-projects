# Humor Detection Project

## Overview

The Humor Detection Project aims to predict whether a given text is humorous or not using machine learning techniques. The project includes data loading, preprocessing, vectorization, model training, and a Streamlit web application for user interaction.

## Data

The project utilizes a dataset with 200,000 observations, each containing a text sample and a flag indicating whether the text is humorous or not.

## Project Structure

The project is structured as follows:

- **main.py**: Script for loading and preprocessing data, vectorizing text using Count Vectorizer and TF-IDF Vectorizer, training and evaluating two machine learning models (Multinomial Naive Bayes and Logistic Regression with Stochastic Gradient Descent), and saving the trained vectorizers and models.

- **UDFs**: A directory containing utility functions/classes for text preprocessing and classification. 
  - `TextPreprocessor`: Class for cleaning and preprocessing text data.
  - `TextClassifier`: Class for text classification using pre-trained models.

- **app.py**: Script for the Streamlit web application. Users can input a text, choose a classifier and vectorizer, and the app predicts whether the text is humorous or not.

- **main-jupyter.ipynb**: Jupyter Notebook version of `main.py`.

## Usage

1. **Install Dependencies**: Make sure to install the required dependencies by running:
   ```bash
   pip install -r requirements.txt