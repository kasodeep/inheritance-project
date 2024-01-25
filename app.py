from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/run_program', methods=['POST'])
def run_program():
    user_input = request.form['user_input']
    result = subprocess.run(['python3', 'PDF.py', user_input], capture_output=True, text=True)
    return result.stdout

if __name__ == '__main__':
    app.run(debug=True)
