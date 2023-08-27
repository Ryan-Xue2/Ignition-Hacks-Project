import re
from keybert import KeyBERT


class QuizFlare:
    def __init__(self):
        self.kb = KeyBERT()

        # Keep track of the user's input, the question generated, and the answer key
        self.text = ''
        self.question = ''
        self.answer_key = []
    
    def create_quiz(self, text):
        """Takes as input a chunk of text and replaces the keywords with blanks"""
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
                new_words.append(f"{'_' * len(word)}<sub>{num_blank}</sub>")
                num_blank += 1
                continue
            new_words.append(word)

        self.question = ''.join(new_words)
        return self.question, self.answer_key
    
    def grade_quiz(self, user_answers):
        """Takes as input a list of the user's answers. Returns the user's mark as well as a list containing feedback for each question"""
        grade = 0
        feedback = []
        for user_answer, true_answer in zip(user_answers, self.answer_key):
            if user_answer.lower().strip() == true_answer:
                feedback.append(f'Incorrect. Correct answer was {true_answer}')
            else:
                feedback.append('Correct!')
                grade += 1
        return grade, feedback