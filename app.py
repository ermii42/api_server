from flask import Flask, request
import logging
import json
from translate import get_translation
from grammar import get_mistakes


app = Flask(__name__)

logging.basicConfig(level=logging.INFO, filename='app.log', format='%(asctime)s %(levelname)s %(name)s %(message)s')
sessionStorage = {}
listening = False
action = None


@app.route('/post', methods=['POST'])
def main():

    logging.info('Request: %r', request.json)

    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }
    try:
        handle_dialog(response, request.json)
    except Exception:
        response['response']['text'] = 'Ой, кажется что-то пошло не так. Сделаем вид, что ничего не произошло.'

    logging.info('Request: %r', response)

    return json.dumps(response)


def handle_dialog(res, req):
    global listening, action
    user_id = req['session']['user_id']
    if listening:
        txt = req['request']["original_utterance"]

        if action == 't':
            answer = get_translation(txt)
        else:
            answer = get_mistakes(txt)

        if answer != 'Ой, я не знаю этот язык! не могли бы вы написать что-либо на русском/английском?':
            listening = False
            action = None

        res['response']['text'] = answer
        return

    if req['session']['new']:
        sessionStorage[user_id] = {
            'suggests': [
                "Алиса, переведи мне текст",
                "Алиса, проверь мое предложение",
            ]
        }

        res['response']['text'] = 'Привет! Я - Алиса-лингвист. Что тебя интересует?'
        res['response']['buttons'] = get_suggests(user_id)

        return

    if 'возможности' in req['request']['nlu']['tokens'] or "команды" in req['request']['nlu']['tokens']:
        sessionStorage[user_id] = {
            'suggests': [
                "Переведи мне текст",
                "Проверь мое предложение",
            ]
        }

        res['response']['text'] = 'Я умею переводить текст с анлийского на русский и с русского на английский!\n' \
                                  'А также проверять твои предложения на грамматические ошибки.\n' \
                                  'Что тебя интересует? :P'
        res['response']['buttons'] = get_suggests(user_id)

        return

    tokens = get_command(req)

    if len(tokens) == 0:
        res['response']['text'] = 'Прости, я не могу понять тебя. Не мог бы ты повторить?'

    elif len(tokens) > 1:
        res['response']['text'] = 'Хей, не все сразу.'

    elif len(tokens) == 1:
        res['response']['text'] = "Я вас внимательно слушаю."
        listening = True
        if tokens[0] == 'переведи':
            action = 't'
        else:
            action = 'g'


def get_suggests(user_id):
    session = sessionStorage[user_id]

    # Выбираем две первые подсказки из массива.
    suggests = [
        {'title': suggest, 'hide': True}
        for suggest in session['suggests']
    ]
    sessionStorage[user_id] = session

    return suggests


def get_command(req):

    tokens = []

    for token in req['request']['nlu']['tokens']:
        if token in ["переведи", "проверь"] and token not in tokens:
            tokens.append(token)

    return tokens


if __name__ == '__main__':
    app.run()
