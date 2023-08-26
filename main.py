from flask import Flask, render_template, request
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/test', methods=['POST'])
def test_page():
    form_data = request.form
    print(form_data)
    return "hi"