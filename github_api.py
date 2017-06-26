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

credentials = ('Genaron', 'd4db47' 'c185c80ca'
						  'e5fbfc35c' 'd2c26d885e98ff7f')

repo_api_url = 'https://api.github.com/repos/Genaron/T07'
print(get_issue(1))
