import os
import time
import flask
import logging
import requests

from mi_bot import start, get, post, label, close, cmd_error


token_bot = '439953184:AAFdqVKqmxFOnKuClHhjCPN0v0Ee1ZmMwZw'
url = 'https://api.telegram.org/bot{}/'.format(token_bot)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
                           '%(message)s', level=logging.INFO)

app = flask.Flask(__name__)
running = False
ids = []


@app.route('/')
def index():
    global running, ids

    if not running:
        running = True
    updates_ini = get_updates()

    while True:
        updates_now = get_updates()
        if len(updates_now['result']) != len(updates_ini['result']):
            updates_ini = updates_now
            last_update = updates_now['result'][-1]
            user = last_update['message']['from']['first_name']
            text = last_update['message']['text']
            chat_id = last_update['message']['from']['id']
            handle_msg(text, user, chat_id)
            if chat_id not in ids:
                ids.append(chat_id)
        time.sleep(0.5)


@app.route('/upload', methods=['POST'])
def receive():
    global running, ids
    if not running:
        return 'El bot se encuentra apagado.'
    if flask.request.headers['content-Type'] == 'application/json':
        return flask.request.json


def get_updates():
    global url
    url_updates = url + 'getUpdates?timeout=100'
    updates = requests.get(url_updates).json()
    return updates


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
