from flask import Flask, request, render_template
import os
import re
from collections import Counter

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return 'Нет файла'
    file = request.files['file']
    if file.filename == '':
        return 'Не выбран файл'
    if file:
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
        most_common_word = find_most_common_word(filepath)
        return f'Самое частое слово: {most_common_word}'

def find_most_common_word(filepath):
    with open(filepath, 'r', encoding='utf-8') as file:
        text = file.read().lower()
        words = re.findall(r'\b\w+\b', text)
        if not words:
            return None
        counter = Counter(words)
        most_common_word, _ = counter.most_common(1)[0]
        return most_common_word

if __name__ == '__main__':
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    app.run(debug=True)