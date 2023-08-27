import random
from testmaster import QuizFlare
from flask import Flask, render_template, request, Markup, session


app = Flask(__name__)
qf = QuizFlare()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    text = request.form.get('text')
    questions, answers = qf.create_quiz(text)
    return render_template('test.html', questions=Markup(questions), answers=answers)


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/results', methods=['POST'])
def results():
    user_answers = []
    for i in range(len(qf.answer_key)):
        user_answers.append(request.form.get(f'{i}'))
    grade, feedback = qf.grade_quiz(user_answers)
    return render_template('results.html', grade=grade, feedback=feedback)


@app.template_filter('uniqueshuffle')
def unique_shuffle(seq):
    """Removes all duplicate items in a sequence and shuffles items"""
    lst = list(set(seq))
    random.shuffle(lst)
    return lst


if __name__ == '__main__':
    app.run()