import requests


def get_translation(text):

    url = "https://translate.yandex.net/api/v1.5/tr.json/translate"
    lang = lg_to_lg(text)

    if lang is None:
        return 'Ой, я не знаю этот язык! не могли бы вы написать что-либо на русском/английском?'

    params = {
        'key': 'trnsl.1.1.20190424T062415Z.70d39808935a81bc.fe2490dd592a3c32800a2c9dcda4df66aac6e672',
        'text': text,
        "lang": lang
    }

    response = requests.get(url, params)
    json = response.json()

    return "Вот, как я это переведу:\n" + "'" + json['text'][0] + "'"


def get_lang(text):
    url = "https://translate.yandex.net/api/v1.5/tr.json/detect"

    params = {
        'key': 'trnsl.1.1.20190424T062415Z.70d39808935a81bc.fe2490dd592a3c32800a2c9dcda4df66aac6e672',
        'text': text
    }
    response = requests.get(url, params)
    json = response.json()
    if json['lang'] in ["en", "ru"]:
        return json['lang']
    return


def lg_to_lg(text):
    lang = get_lang(text)
    if lang is None:
        return
    if lang == 'ru':
        return 'ru-en'
    return 'en-ru'
