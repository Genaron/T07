import flask


app = flask.Flask(__name__)


@app.route('/')
def index():
    return '<h1>Bienvenido a nuestro primer Web Service!</h1><br/>' \
           'Aquí podrás escribir en HTML como si fuera una página ' \
           'Web cualquiera.'

app.run()
