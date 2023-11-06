import pandas as pd
import numpy as np
title_basics = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/title.basics.tsv", sep="\t", quoting=3,
                           encoding='latin-1',
                           engine='python', nrows=50)
ratings = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/ratings.tsv", sep="\t", quoting=3, encoding='latin-1',
                      engine='python', nrows=50)
info_person = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/name.tsv", sep="\t", quoting=3, encoding='latin-1',
                          engine='python', nrows=50)


# print(ratings['averageRating'].loc[0])
# f"{info_person['birthYear'].loc[0]}"
# f"{title_basics['originalTitle'].loc[11]}"
#  f"{info_person['primaryProfession'].loc[1]}"]

# questions_easy = [f"What is the birth year of {info_person['primaryName'].loc[0]}?",
#    f"What is the original title of {title_basics['primaryTitle'].loc[11]}?",
#    f"What are the primary professions of {info_person['primaryName'].loc[1]}"]

# answers = [()]




rt = np.random.choice(title_basics['tconst'])
question = f"In quale anno è uscito {title_basics.loc[title_basics['tconst'] == rt, 'primaryTitle'].values[0]}?"
print(question)
answer = f"{title_basics.loc[title_basics['tconst'] == rt, 'startYear'].values[0]}"
print(answer)




