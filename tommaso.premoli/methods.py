import pandas as pd
from numpy import random
import string
import matplotlib.pyplot as plt


class play_quiz:
    def __init__(self, dataset_path):
        self.movies = pd.read_excel(dataset_path)
        self.movies['genres'] = self.movies['genres'].str.lower()
        self.movies.dropna(inplace=True)
        self.movies['year'] = pd.to_numeric(self.movies['year'], errors='coerce').fillna(0).astype(int)

    def format_genres(self, genres):
        genres = genres.split('|')
        if len(genres) > 1:
            genres = ', '.join(genres[:-1]) + ' and ' + genres[-1]
        else:
            genres = genres[0]
        return genres

    def choose_difficulty(self):
        difficulty = input("Choose your difficulty level (Easy/Difficult): ").lower()
        if difficulty == 'easy':
            return self.movies['year'] > 1990
        elif difficulty == 'difficult':
            return self.movies['year'] < 1990
        else:
            print("Invalid choice, defaulting to Easy")
            return self.movies['year'] > 1990

    def generate_question(self, difficulty_filter):
        correct_movie = self.movies[difficulty_filter].sample(1)
        question = f"What is the title of the film released in {correct_movie['year'].values[0]} directed by {correct_movie['director_name'].values[0]}, starring {correct_movie['actor_name'].values[0]}, produced in {correct_movie['country'].values[0]} and belonging to the genre {correct_movie['genres'].values[0]}?"
        return question, correct_movie

    def generate_answers(self, correct_movie):
        incorrect_movies = self.movies.drop(correct_movie.index.values.tolist())
        incorrect_answers = incorrect_movies.sample(3)['movie_title'].values
        correct_answer = correct_movie['movie_title'].values[0]
        answers = [correct_answer] + list(incorrect_answers)
        random.shuffle(answers)
        return answers

    def quiz(self):
        difficulty_filter = self.choose_difficulty()
        score = 0
        score_history = [0]
        for i in range(1, 11):
            question, correct_movie = self.generate_question(difficulty_filter)
            answers = self.generate_answers(correct_movie)
            print(f"Question {i}. {question}")
            for j, answer in zip(string.ascii_uppercase, answers):
                print(f"{j}. {answer}")
            user_answer = input("Your answer: ").upper()
            while user_answer not in string.ascii_uppercase:
                print("You have another chance, try again!")
                user_answer = input("Your answer: ").upper()
            correct_answer = correct_movie['movie_title'].values[0]
            selected_answer = answers[string.ascii_uppercase.index(user_answer)]
            if selected_answer == correct_answer:
                print("Correct!\n")
                score += 1
                score_history.append(score)
            else:
                print(f"Wrong! The correct answer is {correct_answer}\n")
                score_history.append(score)
        print(f"Your total score is {score}/10!\n")
        plt.plot(score_history)
        plt.xlabel('Question number')
        plt.ylabel('Score')
        plt.title('Score over time')
        plt.ylim(0, 10)
        plt.show()
        retry = input("Do you want to retry? (yes/no): ").lower()
        if retry != 'no':
            self.quiz()
        else:
            print("\nThanks for trying!")


