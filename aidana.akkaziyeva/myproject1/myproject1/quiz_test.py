import random
import pandas as pd
import data_generator
netflix_data = pd.read_csv('netflix_data.csv')


question, correct_answer, incorrect_answers = data_generator.generate_question(netflix_data)

print(f"Question: {question}")
print(f"Correct Answer: {correct_answer}")
print(f"Incorrect Answers: {incorrect_answers}")
