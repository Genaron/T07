import re
import logging

from github_api import get_issue, post_comment, add_label, close_issue


def start(bot, update):
	text = 'Hola {}!\n'.format(update.message.from_user.first_name)
	text += 'Soy PrograBot! Con mi ayuda, podrás manejar algunas funcional'
	text += 'idades de los issues presentes en el repositorio https://github.co'
	text += 'm/Genaron/T07\n-------------\nCOMANDOS:\n/get #num_issue:'
	text += 'Se obtiene la información asociada a la issue correspondiente.\n'
	text += '/post #num_issue *respuesta: Se responde la issue correspondiente '
	text += 'con la respuesta entregada.\n/label #num_issue *label: Se asigna l'
	text += 'a etiqueta indicada al issue correspondiente.\n/close #num_issue: '
	text += 'se cierra la issue indicada.\n-------------\nNota: no escribir el '
	text += '\'#\' ni el \'*\' al momento de llamar a los comandos anteriores.'
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


def post(bot, update):
	user = update.message.from_user.first_name

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
		bot.send_message(chat_id=update.message.chat_id, text=text)
	else:
		cmd_error(bot, update)


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
		bot.send_message(chat_id=update.message.chat_id, text=text)
	else:
		cmd_error(bot, update)


def close(bot, update):
	comando = ''
	for s in 'close':
		comando += '({}|{})'.format(s, s.upper())
	pattern = '^/{} \d+$'.format(comando)

	msg = update.message.text
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
		bot.send_message(chat_id=update.message.chat_id, text=text)
	else:
		cmd_error(bot, update)
