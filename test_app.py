import unittest
import os
from app import app, find_most_common_word

class FlaskTestCase(unittest.TestCase):
    def setUp(self):
        app.config['TESTING'] = True
        app.config['UPLOAD_FOLDER'] = 'test_uploads'
        self.app = app.test_client()
        if not os.path.exists(app.config['UPLOAD_FOLDER']):
            os.makedirs(app.config['UPLOAD_FOLDER'])

    def tearDown(self):
        for file in os.listdir(app.config['UPLOAD_FOLDER']):
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file)
            if os.path.isfile(file_path):
                os.unlink(file_path)

    def test_upload_file(self):
        with open('test_file.txt', 'w', encoding='utf-8') as f:
            f.write('hello world hello')
        data = {
            'file': (open('test_file.txt', 'rb'), 'test_file.txt')
        }
        response = self.app.post('/upload', data=data, content_type='multipart/form-data')
        print(f"Test Загрузка файла - Вывод программы: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Самое частое слово: hello', response.get_data(as_text=True))
        os.remove('test_file.txt')

    def test_find_most_common_word(self):
        with open('test_file.txt', 'w', encoding='utf-8') as f:
            f.write('hello world hello')
        most_common_word = find_most_common_word('test_file.txt')
        print(f"Test Нахождение самого частого слова - Самое частое слово: {most_common_word}")
        self.assertEqual(most_common_word, 'hello')
        os.remove('test_file.txt')

    def test_case_insensitivity(self):
        with open('test_file.txt', 'w', encoding='utf-8') as f:
            f.write('Hello hello HELLO world world world')
        most_common_word = find_most_common_word('test_file.txt')
        print(f"Test Влияет ли регистр - Самое частое слово: {most_common_word}")
        self.assertEqual(most_common_word, 'hello')
        os.remove('test_file.txt')
    def test_empty_file(self):
        with open('test_file.txt', 'w', encoding='utf-8') as f:
            f.write('')
        most_common_word = find_most_common_word('test_file.txt')
        print(f"Test Что, если файл пустой - Вывод программы: {most_common_word}")
        self.assertEqual(most_common_word, None)
        os.remove('test_file.txt')

    def test_multiple_common_words(self):
        with open('test_file.txt', 'w', encoding='utf-8') as f:
            f.write('cat dog cat dog')
        most_common_word = find_most_common_word('test_file.txt')
        print(f"Test Несколько самых длинных слов: cat/dog - Вывод программы: {most_common_word}")
        self.assertIn(most_common_word, ['cat', 'dog'])
        os.remove('test_file.txt')

    def test_no_file_selected(self):
        response = self.app.post('/upload', data={}, content_type='multipart/form-data')
        print(f"Test Что если нет файла - Вывод программы: {response.get_data(as_text=True)}")
        self.assertEqual(response.status_code, 200)
        self.assertIn('Нет файла', response.get_data(as_text=True))

if __name__ == '__main__':
    unittest.main(verbosity=2)
