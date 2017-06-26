import os
import logging
import requests
from mi_bot import start, get, post, label, close
from flask import Flask


token_bot = '439953184:AAFdqVKqmxFOnKuClHhjCPN0v0Ee1ZmMwZw'
url = 'https://api.telegram.org/bot{}/'.format(token_bot)

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
						   '%(message)s', level=logging.INFO)

app = Flask(__name__)


@app.route('/')
def index():
	updates_ini = get_updates()
	while True:
		updates_now = get_updates()
		if len(updates_now['result']) != len(updates_ini['result']):
			updates_ini = updates_now
			last_update = updates_now['result'][-1]
			text = last_update['message']['text']
			chat_id = last_update['from']['id']
			send_msg(text, chat_id)


def send_msg(text, chat_id):
	global url
	url_msg = url + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
	requests.get(url_msg)


def get_updates():
	global url
	url_updates = url + 'getUpdates'  # '?timeout=100'
	updates = requests.get(url_updates).json()
	return updates


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	app.run(host='https://heroku-app-t07.herokuapp.com/', port=port)
