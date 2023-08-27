import random
from markupsafe import Markup 
from testmaster import QuizFlare
from flask import Flask, render_template, request


app = Flask(__name__)
qf = QuizFlare()  # Class to manage creating and grading quizzes


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    text = request.form.get('text')
    quiz, answers = qf.create_quiz(text)
    return render_template('test.html', quiz=Markup(quiz), answers=answers)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/results', methods=['POST', 'GET'])
def results():
    if request.method == 'POST':
        # User just submitted their answers so grade their quiz
        user_answers = []
        for i in range(len(qf.answer_key)):
            user_answers.append(request.form.get(f'{i}'))
        qf.grade_quiz(user_answers)

    return render_template('results.html', quiz=Markup(qf.quiz), grade=qf.user_grade, 
                           user_answers=qf.user_answers, feedback=qf.feedback)


@app.template_filter('uniqueshuffle')
def unique_shuffle(seq):
    """Removes all duplicate items in a sequence and shuffles items"""
    lst = list(set(seq))
    random.shuffle(lst)
    return lst


if __name__ == '__main__':
    app.run()