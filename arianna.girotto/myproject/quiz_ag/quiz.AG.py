import pandas as pd
import numpy as np

title_basics = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/title.basics.tsv", sep="\t", quoting=3, encoding='latin-1',
                           engine='python', nrows=10000)
ratings = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/ratings.tsv", sep="\t", quoting=3, encoding='latin-1',
                      engine='python', nrows=10000)
info_person = pd.read_csv("//Users/ariannagirotto/Desktop/dataset/name.tsv", sep="\t", quoting=3, encoding='latin-1',
                          engine='python', nrows=10000)

def generate_question_answers_tb(num_q_title_basics):
    questions = []
    answers_list = []
    for i in range(num_q_title_basics):
        valid_movie = False
        while not valid_movie:
            random_tconst = np.random.choice(title_basics['tconst'], replace=False)
            right_answer = title_basics.loc[title_basics['tconst'] == random_tconst, 'startYear'].values[0]

            # Controlla se right_answer è diverso da '\\N' prima di convertirlo in un intero
            if right_answer != '\\N':
                right_answer = int(right_answer)
                if 1990 <= right_answer <= 2023:
                    valid_movie = True

        if valid_movie:
            movie_title = title_basics.loc[title_basics['tconst'] == random_tconst, 'primaryTitle'].values[0]
            questions.append(f"In quale anno è uscito {movie_title}?")

            wrong_answers = []
            while len(wrong_answers) < 3:
                wrong_answer = np.random.choice(title_basics['startYear'])
                if wrong_answer != '\\N':
                    wrong_answer = int(wrong_answer)
                    if wrong_answer != right_answer and wrong_answer not in wrong_answers and 1990 <= wrong_answer <= 2023:
                        wrong_answers.append(wrong_answer)

            answers = {
                'correct': right_answer,
                'incorrect': wrong_answers
            }
            answers_list.append(answers)

    return questions, answers_list


def generate_question_answers_ip(num_q_info_person):
    questions = []
    answers_list = []
    for j in range(num_q_info_person):
        random_person = np.random.choice(info_person['nconst'], replace=False)
        person_name = info_person.loc[info_person['nconst'] == random_person, 'primaryName'].values[0]
        questions.append(f"Quali sono le principali professioni di {person_name}?")

        right_answer = info_person.loc[info_person['nconst'] == random_person, 'primaryProfession'].values[0]
        wrong_answers = []
        while len(wrong_answers) < 3:
            wrong_answer = np.random.choice(info_person['primaryProfession'])
            if wrong_answer != right_answer and wrong_answer not in wrong_answers:
                wrong_answers.append(wrong_answer)
        answers = {
            'correct': right_answer,
            'incorrect': wrong_answers
        }
        answers_list.append(answers)
    return questions, answers_list


## stiamo definendo una funzione che ha come input il numero di domande che vogliamo generare di un tipo o dell'altro.
## all'interno di questa si crea una variabile denominata 'questions' che servirà a contenere le domande che si creano
## con una lista(in questo modo posso fare append).
## per inserire le domande utilizzo 2 loop per cui per ogni elemento che è all'interno del range del numero delle domande
## (che inserisco io quando utilizzo la funzione) deve randomizzare una tconst, una person, poi creare 2 varibiali una con il
## nome del film e l'altra con il nome della persona e poi fare question append con i due pattern
## infine mi deve ritornare le domande

## per cui moh se scrivo il numero di domande che voglio di ciascun pattern

## distinguo i 3 quiz tra facile, medio e difficile con la percentuale di passaggio, per cui è facile se passi
## con il 50% delle risposte esatte, medio se 60%, difficile se 70%.

def easy():
    title_basics_questions, title_basics_answers = generate_question_answers_tb(1)
    info_person_questions, info_person_answers = generate_question_answers_ip(1)

    title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
    info_person_pairs = list(zip(info_person_questions, info_person_answers))
    pairs = title_basics_pairs + info_person_pairs
    np.random.shuffle(pairs)
    questions, answers = zip(*pairs)

    score = 0

    for i, question in enumerate(questions):
        print(f"Domanda {i + 1}: {question}")
        answer_options = [answers[i]['correct']] + answers[i]['incorrect']
        np.random.shuffle(answer_options)

        for j, answer in enumerate(answer_options):
            print(f"{j + 1}. {answer}")

        while True:
            user_answer = input("Inserisci il numero della risposta corretta: ")
            try:
                user_answer = int(user_answer)
                if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i]['correct']:
                    print("Risposta corretta!\n")
                    score += 1
                    break
                elif user_answer > len(answer_options):
                    print("Risposta non valida.\n")
                else:
                    print("Risposta errata!\n")
                    break
            except ValueError:
                print("Inserisci un numero valido.\n")

        print(f"Punteggio finale: {score}/{len(questions)}")

def medium():
    title_basics_questions, title_basics_answers = generate_question_answers_tb(1)
    info_person_questions, info_person_answers = generate_question_answers_ip(1)

    title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
    info_person_pairs = list(zip(info_person_questions, info_person_answers))
    pairs = title_basics_pairs + info_person_pairs
    np.random.shuffle(pairs)
    questions, answers = zip(*pairs)

    score = 0

    for i, question in enumerate(questions):
        print(f"Domanda {i + 1}: {question}")
        answer_options = [answers[i]['correct']] + answers[i]['incorrect']
        np.random.shuffle(answer_options)

        for j, answer in enumerate(answer_options):
            print(f"{j + 1}. {answer}")

        while True:
            user_answer = input("Inserisci il numero della risposta corretta: ")
            try:
                user_answer = int(user_answer)
                if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i]['correct']:
                    print("Risposta corretta!\n")
                    score += 1
                    break
                elif user_answer > len(answer_options):
                    print("Risposta non valida.\n")
                else:
                    print("Risposta errata!\n")
                    break
            except ValueError:
                print("Inserisci un numero valido.\n")

    print(f"Punteggio finale: {score}/{len(questions)}")


def difficult():
    title_basics_questions, title_basics_answers = generate_question_answers_tb(10)
    info_person_questions, info_person_answers = generate_question_answers_ip(10)

    title_basics_pairs = list(zip(title_basics_questions, title_basics_answers))
    info_person_pairs = list(zip(info_person_questions, info_person_answers))
    pairs = title_basics_pairs + info_person_pairs
    np.random.shuffle(pairs)
    questions, answers = zip(*pairs)

    score = 0

    for i, question in enumerate(questions):
        print(f"Domanda {i + 1}: {question}")
        answer_options = [answers[i]['correct']] + answers[i]['incorrect']
        np.random.shuffle(answer_options)

        for j, answer in enumerate(answer_options):
            print(f"{j + 1}. {answer}")

        while True:
            user_answer = input("Inserisci il numero della risposta corretta: ")
            try:
                user_answer = int(user_answer)
                if 1 <= user_answer <= len(answer_options) and answer_options[user_answer - 1] == answers[i]['correct']:
                    print("Risposta corretta!\n")
                    score += 1
                    break
                elif user_answer > len(answer_options):
                    print("Risposta non valida.\n")
                else:
                    print("Risposta errata!\n")
                    break
            except ValueError:
                print("Inserisci un numero valido.\n")

    print(f"Punteggio finale: {score}/{len(questions)}")


def choose_quiz():
    while True:
        choosen_quiz = False
        while not choosen_quiz:
            user_answer = input("Inserisci il quiz che vuoi fare tra easy, medium e difficult: ")
            if user_answer == "easy":
                easy()
                choosen_quiz = True
            elif user_answer == "medium":
                medium()
                choosen_quiz = True
            elif user_answer == "difficult":
                difficult()
                choosen_quiz = True
            else:
                print("Quiz non valido. Inserisci un quiz valido.")
        repeat = input("Vuoi ripetere il quiz? (Sì o No): ")
        if repeat.lower() != "sì":
            break


choose_quiz()

