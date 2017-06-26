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
	return get_updates()


def send_msg(text, chat_id):
	global url
	url_msg = url + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)


def get_updates():
	global url
	url_updates = url + 'getUpdates'
	updates = requests.get(url_updates).json()
	return updates


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	app.run(host='https://heroku-app-t07.herokuapp.com/', port=port)
