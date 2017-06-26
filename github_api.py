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

with open('credentials') as f:
	credentials = tuple(f.read().splitlines())

repo_api_url = 'https://api.github.com/repos/Genaron/T07'
