import os
import requests
import subprocess
from flask import Flask


subprocess.Popen('mi_bot.py')
app = Flask(__name__)


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 8080))
    app.run(host='https://heroku-app-t07.herokuapp.com/', port=port)
