import random
import requests


def get_issue(numero):
	global repo_api_url, credentials
	issue_url = repo_api_url + '/issues/' + str(numero)
	req = requests.get(issue_url, auth=credentials)
	if ('message', 'Not Found') in req.json().items():
		return
	issue_dict = req.json()
	state = issue_dict['state']
	numero = issue_dict['number']
	autor = issue_dict['user']['login']
	titulo = issue_dict['title']
	texto = issue_dict['body']
	url = issue_dict['html_url']
	return state, numero, autor, titulo, texto, url


def post_comment(numero, respuesta):
	global repo_api_url, credentials
	comment_url = repo_api_url + '/issues/{}/comments'.format(numero)
	params = {'body': respuesta}
	req = requests.post(comment_url, json=params, auth=credentials)
	return req.status_code


def add_label(numero, label):
	global repo_api_url, credentials
	labels_url = repo_api_url + '/labels'
	labels = requests.get(labels_url, auth=credentials).json()

	# Vemos si el label existe o no en el repositorio
	existe = False
	for lab in labels:
		if lab['name'] == label:
			existe = True
			break

	# Si no existe, lo generamos con un color aleatorio
	if not existe:
		posibles = '0123456789abcdef'
		color = ''
		for _ in range(6):
			color += random.choice(posibles)
		params = {'name': label, 'color': color}
		requests.post(labels_url, json=params, auth=credentials)

	# Ahora vemos si el label esta en el issue correspondiente
	issue_labels_url = repo_api_url + '/issues/{}/labels'.format(numero)
	list_labels = requests.get(issue_labels_url, auth=credentials).json()
	for lab in list_labels:
		if lab['name'] == label:
			return 'El label solicitado ya existía en esta issue!'
	req = requests.post(issue_labels_url, json=[label], auth=credentials)
	if req.status_code == 200:
		return 'Label agregada con éxito!'
	return 'No se pude agregar el label.'

credentials = ('PrograBot', 'b9ef83adb7f2525329' 'ba54724bb3d842ce3c104f')

repo_api_url = 'https://api.github.com/repos/Genaron/T07'
