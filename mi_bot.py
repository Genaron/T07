import re
import requests

from github_api import get_issue, post_comment, add_label, close_issue


token_bot = '439953184:AAFdqVKqmxFOnKuClHhjCPN0v0Ee1ZmMwZw'
url = 'https://api.telegram.org/bot{}/'.format(token_bot)


def start(user, chat_id):
    text = 'Hola {}!'.format(user)
#    text += 'Soy PrograBot! Con mi ayuda, podrás manejar algunas funcional'
#    text += 'idades de los issues presentes en el repositorio https://github.co'
#    text += 'm/Genaron/T07-------------COMANDOS:/get #num_issue:'
#    text += 'Se obtiene la información asociada a la issue correspondiente. '
#    text += '/post #num_issue *respuesta: Se responde la issue correspondiente '
#    text += 'con la respuesta entregada. /label #num_issue *label: Se asigna l'
#    text += 'a etiqueta indicada al issue correspondiente. /close #num_issue: '
#    text += 'se cierra la issue indicada.-------------Nota: no escribir el '
#    text += '# ni el * al momento de llamar a los comandos anteriores.'
    send_msg(text, chat_id)


def cmd_error(chat_id):
    text = 'El comando ingresado no es válido. Use /start para ver la lista '
    text += 'de comandos.'
    send_msg(text, chat_id)


def get(msg, chat_id):
    comando = ''
    for s in 'get':
        comando += '({}|{})'.format(s, s.upper())
    pattern = '^/{} \d+$'.format(comando)

    if bool(re.match(pattern, msg)):
        issue_id = msg.split(' ')[1]
        items = get_issue(issue_id)
        if items is None:
            text = 'No existe la issue {}'.format(issue_id)
        else:
            state, numero, autor, titulo, texto, url_ = items
            if state == 'closed':
                text = 'La issue {} ya fue resuelta.'.format(issue_id)
            else:
                text = 'La issue {} no ha sido resuelta.'.format(issue_id)
            text += '------------'
            text += '[autor: {}]------------'.format(autor)
            text += '[#{} - {}]------------'.format(numero, titulo)
            text += texto + '------------' + url_
        send_msg(text, chat_id)
    else:
        cmd_error(chat_id)


def post(msg, user, chat_id):
    comando = ''
    for s in 'post':
        comando += '({}|{})'.format(s, s.upper())
    pattern = '^/{} \d+ (\s|\S)+'.format(comando)

    if bool(re.match(pattern, msg)):
        space_1 = msg.find(' ')
        space_2 = msg.find(' ', space_1 + 1)
        issue_id = msg[space_1 + 1: space_2]
        respuesta = msg[space_2 + 1:]
        items = get_issue(issue_id)
        if items is None:
            text = 'No existe la issue {}'.format(issue_id)
        elif items[0] == 'closed':
            text = 'La issue {} ya está cerrada.'.format(issue_id)
        else:
            signature = '\n\n----------\nRespuesta generada por {} desde ' \
                        '@GenaroLaymunsBot de Telegram.'.format(user)
            status = post_comment(issue_id, respuesta + signature)
            if status == 201:
                text = 'Issue número {} respondida con éxito! Para ver el ' \
                       'issue con los comentarios, ingrese a https://github' \
                       '.com/Genaron/T07/issues/{}'.format(issue_id, issue_id)
            else:
                text = 'No fue posible comentar el issue.'
        send_msg(text, chat_id)
    else:
        cmd_error(chat_id)


def label(msg, chat_id):
    comando = ''
    for s in 'label':
        comando += '({}|{})'.format(s, s.upper())
    pattern = '^/{} \d+ \w+$'.format(comando)

    if bool(re.match(pattern, msg)):
        space_1 = msg.find(' ')
        space_2 = msg.find(' ', space_1 + 1)
        issue_id = msg[space_1 + 1: space_2]
        new_label = msg[space_2 + 1:]

        items = get_issue(issue_id)
        if items is None:
            text = 'No existe la issue {}'.format(issue_id)
        elif items[0] == 'closed':
            text = 'La issue {} ya está cerrada.'.format(issue_id)
        else:
            text = add_label(issue_id, new_label)
            text += ' Para ver el issue correspondiente, ingrese a ' \
                    'https://github.com/Genaron/T07/issues/{}' \
                    ''.format(issue_id)
        send_msg(text, chat_id)
    else:
        cmd_error(chat_id)


def close(msg, chat_id):
    comando = ''
    for s in 'close':
        comando += '({}|{})'.format(s, s.upper())
    pattern = '^/{} \d+$'.format(comando)

    if bool(re.match(pattern, msg)):
        issue_id = msg.split(' ')[1]

        items = get_issue(issue_id)
        if items is None:
            text = 'No existe la issue {}'.format(issue_id)
        elif items[0] == 'closed':
            text = 'La issue {} ya estaba cerrada.'.format(issue_id)
        else:
            text = close_issue(issue_id)
            text += ' Para ver el issue correspondiente, ingrese a ' \
                    'https://github.com/Genaron/T07/issues/{}' \
                    ''.format(issue_id)
        send_msg(text, chat_id)
    else:
        cmd_error(chat_id)


def send_msg(text, chat_id):
    global url
    url_msg = url + 'sendMessage?text={}&chat_id={}'.format(text, chat_id)
    requests.get(url_msg)
