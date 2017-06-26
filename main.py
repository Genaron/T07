import os
import subprocess
from flask import Flask


subprocess.Popen('mi_bot.py')
app = Flask(__name__)


@app.route('/')
def index():
	return 'El servidor está arriba!'

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8080))
	app.run(host='https://heroku-app-t07.herokuapp.com/', port=port)
