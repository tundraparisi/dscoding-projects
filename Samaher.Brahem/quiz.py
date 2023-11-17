
import random

class Quiz:
    def __init__(self, movie_data):
        self.movie_data = movie_data

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
    
    def generate_question(self, row, desired_difficulty, question_type, correct_answer_column):
        official_title = row['official_title']
        correct_answer = row[correct_answer_column]

        year = int(row['year']) 
        votes = int(row['votes'])
        difficulty_level = self.determine_difficulty_level(year, votes)

        if difficulty_level == desired_difficulty:
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

    def quiz_game(self):
        if self.movie_data is None:
            raise ValueError("Movie data is required to play the quiz.")

        difficulty_levels = ['easy', 'medium', 'hard']
        total_score = 0
        used_questions = []

        user_difficulty = input("Choosing a difficulty level (easy, medium, hard): ").lower()

        while user_difficulty not in difficulty_levels:
            print("Invalid difficulty level. Please choose from: easy, medium, hard")
            user_difficulty = input("Choosing a difficulty level (easy, medium, hard): ").lower()

        question_generators = [
            {'generator': self.generate_question, 'params': ('When was this movie released? ==> ', 'year')},
            {'generator': self.generate_question, 'params': ('Where was this movie produced? ==> ', 'country')}
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
                user_choice = input("Entering your choice (A, B, C, D): ").upper()

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

        print(f"Total score: {total_score}")
