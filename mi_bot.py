import re
import logging

from github_api import get_issue
from telegram.ext import (Updater, CommandHandler, MessageHandler, Filters)


token_bot = '439953184:AAFdqVKqmxFOnKuClHhjCPN0v0Ee1ZmMwZw'
updater = Updater(token=token_bot)
dispatcher = updater.dispatcher
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - '
							'%(message)s', level=logging.INFO)


def start(bot, update):
	text = 'Hola! Soy PrograBot! Con mi ayuda, podrás manejar algunas funcional'
	text += 'idades de los issues presentes en el repositorio https://github.co'
	text += 'm/Genaron/T07\n-------------\nCOMANDOS:\n/get #num_issue:'
	text += 'Se obtiene la información asociada a la issue correspondiente.\n'
	text += '/post #num_issue *respuesta: Se responde la issue correspondiente '
	text += 'con la respuesta entregada.\n/label #num_issue label: Se asigna la'
	text += ' etiqueta indicada al issue correspondiente.\n/close #num_issue: '
	text += 'se cierra la issue indicada.'
	bot.send_message(chat_id=update.message.chat_id, text=text)


def cmd_error(bot, update):
	text = 'El comando ingresado no es válido. Use /start para ver la lista '
	text += 'de comandos.'
	bot.send_message(chat_id=update.message.chat_id, text=text)


def get(bot, update):
	comando = ''
	for s in 'get':
		comando += '({}|{})'.format(s, s.upper())
	pattern = '^/{} \d+$'.format(comando)

	msg = update.message.text
	if bool(re.match(pattern, msg)):
		issue_id = msg.split(' ')[1]
		items = get_issue(issue_id)
		if items is None:
			text = 'No existe la issue {}'.format(issue_id)
		else:
			state, numero, autor, titulo, texto, url = items
			if state == 'closed':
				text = 'La issue {} ya fue resuelta.\n\n'.format(issue_id)
			else:
				text = 'La issue {} no ha sido resuelta.\n\n'.format(issue_id)
			text += '[autor: {}]\n\n'.format(autor)
			text += '[#{} - {}]\n\n'.format(numero, titulo)
			text += texto + '\n\n' + url
		bot.send_message(chat_id=update.message.chat_id, text=text)
	else:
		cmd_error(bot, update)


# todo
def post(bot, update):
	comando = ''
	for s in 'post':
		comando += '({}|{})'.format(s, s.upper())
	pattern = '^/{} \d+ (\s|\S)+'.format(comando)

	msg = update.message.text
	if bool(re.match(pattern, msg)):
		space_1 = msg.find(' ')
		space_2 = msg.find(' ', space_1 + 1)
		issue_id = msg[space_1 + 1: space_2]
		respuesta = msg[space_2 + 1:]
		text = 'Issue número: {}\nRespuesta: {}'.format(issue_id, respuesta)
		bot.send_message(chat_id=update.message.chat_id, text=text)
	else:
		cmd_error(bot, update)


# todo
def label(bot, update):
	comando = ''
	for s in 'label':
		comando += '({}|{})'.format(s, s.upper())
	pattern = '^/{} \d+ \w+$'.format(comando)

	msg = update.message.text
	if bool(re.match(pattern, msg)):
		space_1 = msg.find(' ')
		space_2 = msg.find(' ', space_1 + 1)
		issue_id = msg[space_1 + 1: space_2]
		new_label = msg[space_2 + 1:]
		text = 'Issue número: {}\nLabel: {}'.format(issue_id, new_label)
		bot.send_message(chat_id=update.message.chat_id, text=text)
	else:
		cmd_error(bot, update)


# todo
def close(bot, update):
	comando = ''
	for s in 'close':
		comando += '({}|{})'.format(s, s.upper())
	pattern = '^/{} \d+$'.format(comando)

	msg = update.message.text
	if bool(re.match(pattern, msg)):
		issue_id = msg.split(' ')[1]
		text = 'Cerrando issue número: {}'.format(issue_id)
		bot.send_message(chat_id=update.message.chat_id, text=text)
	else:
		cmd_error(bot, update)


start_handler = CommandHandler('start', start)
dispatcher.add_handler(start_handler)

get_handler = CommandHandler('get', get)
dispatcher.add_handler(get_handler)

post_handler = CommandHandler('post', post)
dispatcher.add_handler(post_handler)

label_handler = CommandHandler('label', label)
dispatcher.add_handler(label_handler)

close_handler = CommandHandler('close', close)
dispatcher.add_handler(close_handler)

echo_handler = MessageHandler(Filters.text, start)
dispatcher.add_handler(echo_handler)

updater.start_polling()
