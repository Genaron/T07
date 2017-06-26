import os
from flask import Flask, request


app = Flask(__name__)


@app.route('/')
def index():
	return 'Hello World!'


@app.route('/api(<api_id>')
def api_get(api_id):
	return '{}: {}'.format(api_id, request.args)


if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	app.run(host='https://heroku-app-t07.herokuapp.com/', port=port)
