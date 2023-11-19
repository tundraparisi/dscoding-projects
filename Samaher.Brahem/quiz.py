import pandas as pd
import numpy as np
import random
import matplotlib.pyplot as plt
import json 

class Quiz:
    def __init__(self, data_frame):
        self.movie_data = data_frame
        self.game_scores = []

    def determine_difficulty_level(self, year, votes):
        if (year >= 2010 and votes >= 500000) or (year < 2010 and votes >= 1000000):
            return 'easy'
        elif 1990 <= year < 2010 and 100000 <= votes < 500000:
            return 'medium'
        elif year < 1990 and votes < 100000:
            return 'hard'
        else:
            return 'unknown'

    def calculate_score(self, difficulty_level, is_correct):
        if is_correct:
            if difficulty_level == 'easy':
                return 1
            elif difficulty_level == 'medium':
                return 2
            elif difficulty_level == 'hard':
                return 3
        else:
            return 0

    def find_highest_score_movie(self, movie_options):
        self.movie_data['score'] = pd.to_numeric(self.movie_data['score'])
        filtered_data = self.movie_data[self.movie_data['official_title'].isin(movie_options)]
        max_score_index = np.argmax(filtered_data['score'].values)
        highest_score_movie = filtered_data.iloc[max_score_index]['official_title']

        return highest_score_movie

    def generate_question(self, row, desired_difficulty, question_type, correct_answer_column):
        official_title = row['official_title']
        correct_answer = row[correct_answer_column]
        year = int(row['year'])
        votes = int(row['votes'])
        difficulty_level = self.determine_difficulty_level(year, votes)

        if difficulty_level == desired_difficulty:
            if question_type == 'Which one of these movies has the highest score on IMDb?':
                all_movies = self.movie_data['official_title']
                # Randomly select 4 movies 
                selected_movies = random.sample(all_movies.tolist(), min(len(all_movies), 4))

                # Find the highest-scored movie among the selected options
                highest_score_movie = self.find_highest_score_movie(selected_movies)

                other_options = selected_movies.copy()
                random.shuffle(other_options)
                options_mapping = {chr(ord('A') + i): option for i, option in enumerate(other_options)}

                # Find the index of the correct answer within the options
                correct_answer_index = -1
                for i, option in enumerate(other_options):
                    if option == highest_score_movie:
                        correct_answer_index = i
                        break

                # Ensure correct_answer_index exists before assigning the correct_answer
                if correct_answer_index != -1:
                    question_dict = {
                        'question': f'{question_type}',
                        'options': options_mapping,
                        'correct_answer': chr(ord('A') + correct_answer_index),
                        'difficulty_level': difficulty_level
                    }
                    return question_dict


            else:
                all_answers = list(set(self.movie_data[correct_answer_column].unique()))
                all_answers.remove(correct_answer)
                other_options = [correct_answer] + random.sample(all_answers, 3)
                random.shuffle(other_options)
                options_mapping = {chr(ord('A') + i): option for i, option in enumerate(other_options)}
                question_dict = {
                    'question': f'{question_type} || {official_title} ||',
                    'options': options_mapping,
                    'correct_answer': chr(ord('A') + other_options.index(correct_answer)),
                    'difficulty_level': difficulty_level
                }
                return question_dict



    def load_scores(self, filename):
        try:
            with open(filename, 'r') as file:
                self.game_scores = json.load(file)
        except FileNotFoundError:
            self.game_scores = []

    def save_scores(self, filename):
        with open(filename, 'w') as file:
            json.dump(self.game_scores, file)



    def display_histogram(self, player_name):
        player_scores = {name: score for name, score in self.game_scores}
        plt.figure(figsize=(10, 6), dpi=80)

        # Extract player names and scores
        names = list(player_scores.keys())
        scores = list(player_scores.values())

        # Get indices to sort scores in descending order
        sorted_indices = np.argsort(scores)[::-1]

        # Rearrange names and scores based on sorted indices
        names = [names[i] for i in sorted_indices]
        scores = [scores[i] for i in sorted_indices]

        # Plotting player scores
        bars = plt.bar(names, scores, color='#202060')

        # Highlight the current player's score in a different color and add data label
        if player_name in player_scores:
            index = names.index(player_name)
            bars[index].set_color('#5bc8af')
            plt.text(index, scores[index], str(scores[index]), ha='center', va='bottom', fontname='Quicksand', fontsize=10)

        plt.xlabel('Players', fontname='Quicksand', fontsize=12)
        plt.ylabel('Scores', fontname='Quicksand', fontsize=12)
        plt.title('Players\' Scores Distribution', fontname='Quicksand', fontsize=16)
        plt.xticks(rotation=45, fontname='Quicksand', fontsize=10)  # Rotate x-axis labels for readability
        plt.yticks(fontname='Quicksand', fontsize=10)
        plt.grid(axis='y')  # Show grid lines only for y-axis
        plt.tight_layout()
        plt.show()



    def quiz_game(self):
        difficulty_levels = ['easy', 'medium', 'hard']
        total_score = 0
        used_questions = []


        print('HELLO THERE! Welcome to ✨ The Quiz ✨')
        player_name = input("What do you want us to call you? ")
        print('Alright, ' + player_name + '!\n GET READY TO PLAY 🔥')
        print("----------------------------")

        user_difficulty = input("Choose a difficulty level (easy, medium, hard): ").lower()
        print("----------------------------")

        while user_difficulty not in difficulty_levels:
            print("Invalid difficulty level. Please choose from: easy, medium, hard")
            user_difficulty = input("Choose a difficulty level (easy, medium, hard): ").lower()

        question_generators = [
            {'generator': self.generate_question, 'params': ('When was this movie released? ==> ', 'year')},
            {'generator': self.generate_question, 'params': ('Where was this movie produced? ==> ', 'country')},
            {'generator': self.generate_question, 'params': ('Which one of these movies has the highest score on IMDb?', 'score')}
        ]

        for i in range(10):
            while True:
                question_info = None
                generator_info = random.choice(question_generators)
                question_type, correct_answer_column = generator_info['params']

                row_index = random.randint(0, len(self.movie_data) - 1)
                row = self.movie_data.iloc[row_index]

                question_info = generator_info['generator'](row, user_difficulty, question_type, correct_answer_column)

                if question_info is not None and question_info['question'] not in used_questions:
                    used_questions.append(question_info['question'])
                    break

            print(question_info['question'])

            for letter, option in question_info['options'].items():
                print(f"{letter}. {option}")

            user_choice = None
            while user_choice not in ['A', 'B', 'C', 'D']:
                user_choice = input("Enter your choice (A, B, C, D): ").upper()

                if user_choice not in ['A', 'B', 'C', 'D']:
                    print("You typed a wrong letter. Please type again.")

            is_correct = user_choice == question_info['correct_answer']
            score = self.calculate_score(question_info['difficulty_level'], is_correct)
            total_score += score

            if is_correct:
                print("Correct!")
            else:
                print(f"Wrong! The correct answer is: {question_info['correct_answer']}")

            print(f"Your score for this question: {score}")
            print("----------------------------")

        game_score = (player_name, total_score)
        self.load_scores('game_scores.json')  # Load existing scores

        # If the player already exists in the scores, update their score
        player_exists = False
        for index, (name, score) in enumerate(self.game_scores):
            if name == player_name:
                player_exists = True
                self.game_scores[index] = (name, score + total_score)
                break

        # If the player doesn't exist, add their score to the list
        if not player_exists:
            self.game_scores.append(game_score)

        print(f"Total score: {total_score}")
        print(f"Here's how you performed, {player_name}:")
        self.display_histogram(player_name)

        self.save_scores('game_scores.json')  # Save scores after each game in JSON format

        return self.game_scores