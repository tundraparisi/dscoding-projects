import random
import pandas as pd
import data_generator
netflix_data = pd.read_csv('netflix_data.csv')

#Checking if my dataframe has duplicate titles
has_duplicates = netflix_data['title'].duplicated().sum()

if has_duplicates > 0:
    print(f"The DataFrame has {has_duplicates} duplicate titles.")
else:
    print("The DataFrame does not have any duplicate titles.")



#Checking if my dataframe has duplicate directors column
has_duplicates = netflix_data['director'].duplicated().sum()

if has_duplicates > 0:
    print(f"The DataFrame has {has_duplicates} duplicate director columns.")
else:
    print("The DataFrame does not have any duplicate director columns.")




question, correct_answer, incorrect_answers = data_generator.generate_genre_question(netflix_data)

print(f"Question: {question}")
print(f"Correct Answer: {correct_answer}")
print(f"Incorrect Answers: {incorrect_answers}")

#data_generator.present_dir_question(question, correct_answer, incorrect_answers)


