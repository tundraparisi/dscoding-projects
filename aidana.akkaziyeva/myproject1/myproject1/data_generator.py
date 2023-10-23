import pandas as pd
import random

netflix_data = pd.read_csv('netflix_data.csv')
#print(netflix_data.head())



def generate_question(netflix_data):
    show = random.choice(netflix_data['title'])
    director = netflix_data.loc[netflix_data['title']==show, 'director'].values[0]
    cast = netflix_data.loc[netflix_data['title']==show, 'cast'].values[0]
    
    question = f"Who directed '{show}'?"
    correct_answer = director
    incorrect_answers = random.sample(list(netflix_data['director'].unique()),3)
   
    return question, correct_answer, incorrect_answers


