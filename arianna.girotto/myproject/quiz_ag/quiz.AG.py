import pandas as pd
import numpy as np

title_basics = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/title.basics.tsv", sep="\t", quoting=3,
                           encoding='latin-1',
                           engine='python', nrows=50)
ratings = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/ratings.tsv", sep="\t", quoting=3, encoding='latin-1',
                      engine='python', nrows=50)
info_person = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/name.tsv", sep="\t", quoting=3, encoding='latin-1',
                          engine='python', nrows=50)


# answer = f"{title_basics.loc[title_basics['tconst'] == rt, 'startYear'].values[0]}"

# def generate_question(title_basics, info_person, num_questions):
#   questions = []
#  for i in range(num_questions):
#     random_tconst = np.random.choice(title_basics['tconst'], replace=False)
#    random_person = np.random.choice(info_person['nconst'], replace=False)
#   movie_title = title_basics.loc[title_basics['tconst'] == random_tconst, 'primaryTitle'].values[0]
#  person_name = info_person.loc[info_person['nconst'] == random_person, 'primaryName'].values[0]
# questions.append(f"In quale anno è uscito {movie_title}?")
# questions.append(f"Quali sono le principali professioni di {person_name}?")
# return questions
# Example usage
# num_questions = int(input("Enter the number of questions you want to generate: "))
# questions = generate_question(title_basics, info_person, num_questions)
# print(questions)


# def generate_question(num_q_title_basics, num_q_info_person):
#   questions = []
#  for i in range(num_q_title_basics):
#     random_tconst = np.random.choice(title_basics['tconst'], replace=False)
#    movie_title = title_basics.loc[title_basics['tconst'] == random_tconst, 'primaryTitle'].values[0]
#   questions.append(f"In quale anno è uscito {movie_title}?")
# for j in range(num_q_info_person):
#   random_person = np.random.choice(info_person['nconst'], replace=False)
#  person_name = info_person.loc[info_person['nconst'] == random_person, 'primaryName'].values[0]
# questions.append(f"Quali sono le principali professioni di {person_name}?")
# return questions


def generate_question_answers(num_q_title_basics, num_q_info_person):
    questions = []
    answers = []

    for i in range(num_q_title_basics):
        random_tconst = np.random.choice(title_basics['tconst'], replace=False)
        movie_title = title_basics.loc[title_basics['tconst'] == random_tconst, 'primaryTitle'].values[0]
        questions.append(f"In quale anno è uscito {movie_title}?")
    for _ in questions:
        right_answer = title_basics.loc[title_basics['tconst'] == random_tconst, 'startYear'].values[0]
        wrong_answers = np.random.choice(title_basics['startYear'], 3, replace=False)
        options = [right_answer, wrong_answers]
        answers.append(options)

    for j in range(num_q_info_person):
        random_person = np.random.choice(info_person['nconst'], replace=False)
        person_name = info_person.loc[info_person['nconst'] == random_person, 'primaryName'].values[0]
        questions.append(f"Quali sono le principali professioni di {person_name}?")
    for _ in questions:
        right_answer = info_person.loc[info_person['nconst'] == random_person, 'primaryProfession'].values[0]
        wrong_answers = np.random.choice(info_person['primaryProfession'], 3, replace=False)
        options = [right_answer, wrong_answers]
        answers.append(options)

    return print(questions, answers)


generate_question_answers(1, 1)


## stiamo definendo una funzione che ha come input il numero di domande che vogliamo generare di un tipo o dell'altro.
## all'interno di questa si crea una variabile denominata 'questions' che servirà a contenere le domande che si creano
## con una lista(in questo modo posso fare append).
## per inserire le domande utilizzo 2 loop per cui per ogni elemento che è all'interno del range del numero delle domande
## (che inserisco io quando utilizzo la funzione) deve randomizzare una tconst, una person, poi creare 2 varibiali una con il
## nome del film e l'altra con il nome della persona e poi fare question append con i due pattern
## infine mi deve ritornare le domande

## per cui moh se scrivo il numero di domande che voglio di ciascun pattern
