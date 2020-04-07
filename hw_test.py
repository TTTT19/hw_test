import unittest
import requests
from unittest.mock import patch
import app


# проверка приложения
class TestFunction(unittest.TestCase):
    def setUp(self):
        self.dirs, self.docs = app.update_date()
        with patch('app.update_date', return_value=(self.dirs, self.docs)):
            with patch('app.input', return_value='q'):
                app.secretary_program_start()

    def test_find_owner(self):
        with patch('app.input', return_value='11-2'):
            self.assertEqual(app.get_doc_owner_name(), "Геннадий Покемонов")

    def test_delete_doc(self):
        docs_before_del = len(self.docs)
        with patch('app.input', return_value='11-2'):
            app.delete_doc()
        self.assertNotEqual(docs_before_del, len(self.docs))


# проверка яндекса
API_KEY = 'trnsl.1.1.20190712T081241Z.0309348472c8719d.0efdbc7ba1c507292080e3fbffe4427f7ce9a9f0'
URL_tanslate = 'https://translate.yandex.net/api/v1.5/tr.json/translate'


def translate_it(text):
    """
    https://translate.yandex.net/api/v1.5/tr.json/translate ?
    key=<API-ключ>
     & text=<переводимый текст>
     & lang=<направление перевода>
     & [format=<формат текста>]
     & [options=<опции перевода>]
     & [callback=<имя callback-функции>]
    :param lang_text:
    :return:
    """

    params = {
        'key': API_KEY,
        'text': text,
        'lang': '{}-{}'.format('en', 'ru'),
    }

    response = requests.get(URL_tanslate, params=params)
    json_ = response.json()
    return json_
    # return ''.join(json_['text'])


class TestFunctionYandex(unittest.TestCase):

    def test_translate(self):
        try:
            self.assertEqual(translate_it('hi')['code'], 200)
        except Exception as e:
            print('Не получен ответ 200')
            print(e.__class__)
        try:
            self.assertEqual(translate_it('hi')['text'][0], "привет")
        except Exception as e:
            print('Ошибка в тексте')
            print(e.__class__)


if __name__ == '__main__':
    unittest.main()
