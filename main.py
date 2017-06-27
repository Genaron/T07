import os
import time
import flask
import logging
import requests

from threading import Thread
from github_api import get_issue
from mi_bot import start, get, post, label, close, cmd_error, send_msg


token_bot = '439953184:AAFdqVKqmxFOnKuClHhjCPN0v0Ee1ZmMwZw'
url = 'https://api.telegram.org/bot{}/'.format(token_bot)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                           '%(message)s', level=logging.INFO)

app = flask.Flask(__name__)
running = False
ids = []


@app.route('/')
def index():
    global running
    if not running:
        running = True
        thread_update = Thread(target=run_updates)
        thread_update.start()
        return 'El servidor ha empezado!'
    return 'El servidor ya está funcionando!'


@app.route('/upload', methods=['POST'])
def receive():
    global running, ids
    if not running:
        return 'El bot se encuentra apagado.'
    if flask.request.headers['content-Type'] == 'application/json':
        event = flask.request.headers['X-GitHub-Event']
        action = flask.request.json['action']
        if [event, action] == ['issues', 'opened']:
            text = 'Se ha abierto una nueva issue!\n\n'
            items = get_issue(flask.request.json['issue']['number'])
            state, numero, autor, titulo, texto, url_ = items
            text += '[autor: {}]\n\n'.format(autor)
            text += '[Issue número {} - {}]\n\n'.format(numero, titulo)
            text += texto + '\n\n' + url_
            for chat_id in ids:
                send_msg(text, chat_id)
        if [event, action] == ['issues', 'labeled']:
            num = flask.request.json['issue']['number']
            text = 'Se ha agregado un nuevo label a la issue {}'.format(num)
            items = get_issue(flask.request.json['issue']['number'])
            state, numero, autor, titulo, texto, url_ = items
            text += '[autor: {}]\n\n'.format(autor)
            text += '[Issue número {} - {}]\n\n'.format(numero, titulo)
            text += texto + '\n\n' + url_
            for chat_id in ids:
                send_msg(text, chat_id)
        if [event, action] == ['issues', 'closed']:
            num = flask.request.json['issue']['number']
            text = 'Se ha cerrado la issue {}!\n\n'.format(num)
            items = get_issue(flask.request.json['issue']['number'])
            state, numero, autor, titulo, texto, url_ = items
            text += '[autor: {}]\n\n'.format(autor)
            text += '[Issue número {} - {}]\n\n'.format(numero, titulo)
            text += texto + '\n\n' + url_
            for chat_id in ids:
                send_msg(text, chat_id)
        return 'Gracias!'
    return 'El formato no es correcto.'


def get_updates(first_id):
    global url
    url_updates = url + 'getUpdates?timeout=100&offset=' + str(first_id)
    updates = requests.get(url_updates).json()
    return updates


def run_updates():
    global ids

    first_id = 1
    updates_ini = get_updates(first_id)
    while True:
        updates_now = get_updates(first_id)
        if len(updates_now['result']) != len(updates_ini['result']) and \
                len(updates_now['result']) > 0:
            updates_ini = updates_now
            last_update = updates_now['result'][-1]
            user = last_update['message']['from']['first_name']
            text = last_update['message']['text']
            chat_id = last_update['message']['from']['id']
            handle_msg(text, user, chat_id)
            if chat_id not in ids:
                ids.append(chat_id)
        if len(updates_now) > 10:
            first_id = get_updates(first_id)['result'][-1]['update_id'] + 1
        time.sleep(0.5)


def handle_msg(text, user, chat_id):
    if text[:6].lower() == '/start':
        start(user, chat_id)
    elif text[:4].lower() == '/get':
        get(text, chat_id)
    elif text[:5].lower() == '/post':
        post(text, user, chat_id)
    elif text[:6].lower() == '/label':
        label(text, chat_id)
    elif text[:6].lower() == '/close':
        close(text, chat_id)
    elif text[0] == '/':
        cmd_error(chat_id)


if __name__ == '__main__':
    local = False
    if local:
        port = int(os.environ.get('PORT', 8080))
        host_local = 'localhost'
        app.run(host=host_local, port=port)
    else:
        app.run()
