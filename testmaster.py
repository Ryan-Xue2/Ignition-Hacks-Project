import re
from keybert import KeyBERT


class QuizFlare:
    def __init__(self):
        self.kb = KeyBERT()

        # Keep track of the user's input, the question generated, and the answer key
        self.text = ''
        self.quiz = ''
        self.answer_key = []

        # Keep track of the user's answers to the questions, the feedback, and their grade
        self.feedback = []
        self.user_grade = 0
        self.user_answers = []
    
    def create_quiz(self, text):
        """
        Takes as input a chunk of text and replaces the keywords with blanks.
        Returns the fill-in-the-blank quiz as well as the answer key.
        """
        num_blank = 1
        self.text = text
        self.answer_key = []

        # Get the important words from the text
        keywords = self.kb.extract_keywords(text)
        keywords = set(x[0] for x in keywords)

        # Split the text into words
        words = re.split('( |\.|\?|!|:|;|,)', text) 
        
        # Replace the keywords with blanks and a subscript number indicating which blank it is referring to
        new_words = []
        for word in words:
            if word.lower() in keywords:
                self.answer_key.append(word)
                new_words.append(f"{'_' * 10}<sub>{num_blank}</sub>")
                num_blank += 1
                continue
            new_words.append(word)

        self.quiz = ''.join(new_words)
        return self.quiz, self.answer_key
    
    def grade_quiz(self, user_answers):
        """
        Takes as input a list of the user's answers. Doesn't return anything but
        sets self.user_answers, self.user_grade, and self.feedback to their 
        respective values.
        """
        grade = 0
        feedback = []
        
        for user_answer, true_answer in zip(user_answers, self.answer_key):
            if user_answer.lower().strip() == true_answer.lower():
                feedback.append('Correct!')
                grade += 1
            else:
                feedback.append(f'Incorrect. Correct answer was {true_answer}')

        self.user_answers = user_answers
        self.user_grade = grade
        self.feedback = feedback