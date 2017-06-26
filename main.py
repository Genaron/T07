import os
from flask import Flask


app = Flask(__name__)


@app.route('/')
def index():
	return 'Hello World!'

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	app.run(host='https://heroku-app-t07.herokuapp.com/', port=port)
