import requests
from translate import get_lang


def get_mistakes(text):

    url = "https://speller.yandex.net/services/spellservice.json/checkText"
    lang = get_lang(text)

    if lang is None:
        return 'Ой, я не знаю этот язык! не могли бы вы написать что-либо на русском/английском?'

    params = {
        'text': text,
        'lang': lang,
    }

    mistakes_list = {}
    response = requests.get(url, params)
    json = response.json()
    for mistake in json:
        mistakes_list[mistake['word']] = mistake['s']
    if len(mistakes_list) == 0:
        return 'Все хорошо, у вас нет ошибок'
    else:
        t = 'Я нашла у вас несколько ошибок, а именно в этих словах:'
        for key in mistakes_list:
            t += '\n' + key + ' (возможно вы имели в виду ' + ', '.join(mistakes_list[key]) + ')'
        return t