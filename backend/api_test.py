import requests


def test_get_autor():
    url = 'https://fakerestapi.azurewebsites.net/api/v1/Authors'
    response = requests.get(url)

    assert response.status_code == 200
    data = response.json()
    print(len(data))


def test_get_autor_id(id=4):
    url = 'https://fakerestapi.azurewebsites.net/api/v1/Authors'
    response = requests.get(f'{url}/{id}')
    result = response.json()
    assert response.status_code == 200
    assert result['id'] == id
    assert result['idBook'] == 1
    assert result['firstName'] == f'First Name {id}'
    assert result['lastName'] == f'Last Name {id}'


def test_post_autor():
    url = 'https://fakerestapi.azurewebsites.net/api/v1/Authors'
    body = {'id': 999,
            'idBook': 45,
            'firstName': 'Pert',
            'lastName': 'Nuns'}
    response = requests.post(url, json=body)
    result = response.json()
    assert response.status_code == 200
    assert result.get('idBook') == 45
    assert result.get('lastName') == 'Nuns'
