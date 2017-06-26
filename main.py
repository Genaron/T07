import os
import requests
import mi_bot

from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
	return 'El servidor está arriba!'


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	app.run(host='https://heroku-app-t07.herokuapp.com/', port=port)
