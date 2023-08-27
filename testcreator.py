import re
from keybert import KeyBERT


class QuizFlare:
    def __init__(self):
        self.kb = KeyBERT()
    
    def create_quiz(self, text):
        """Takes as input a chunk of text and """
        keywords = self.kb.extract_keywords(text)
        keywords = set(x[0] for x in keywords)

        words = re.split('( |\.|\?|!|:|;|,)', text) # Split the text into words

        num_blank = 1
        answers = []
        
        new_words = []
        for word in words:
            if word.lower() in keywords:
                answers.append(word)
                new_words.append(f"{'_' * len(word)}<sub>{num_blank}</sub>")
                num_blank += 1
                continue
            new_words.append(word)

        print(''.join(new_words))
        return ''.join(new_words), answers