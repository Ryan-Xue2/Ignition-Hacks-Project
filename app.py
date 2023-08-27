from flask import Flask, render_template, request, Markup
from testcreator import QuizFlare

app = Flask(__name__)
qf = QuizFlare()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/test', methods=['POST'])
def test():
    info = request.form.get('info')
    questions, answers = qf.create_quiz(info)
    return render_template('test.html', questions=Markup(questions), answers=answers)


@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run()