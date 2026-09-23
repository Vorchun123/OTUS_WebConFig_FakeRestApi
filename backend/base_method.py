import requests


class BaseMethod:
    Base_URL = 'https://fakerestapi.azurewebsites.net/api/v1/'

    def __init__(self, base_url=Base_URL):
        self.base_url = base_url

    def request(self, method, endpoint, body=None):
        url = f'{self.base_url}{endpoint}'
        response = requests.request(method, url, json=body)
        response.raise_for_status()
        if not response.content:
            return None
        try:
            return response.json()
        except ValueError:
            return response.text

    def method_get(self, endpoint):
        return self.request('GET', endpoint)

    def method_post(self,endpoint, body):
        return self.request('POST', endpoint, body)

    def method_put(self, endpoint, body):
        return self.request('PUT', endpoint, body)

    def method_delete(self, endpoint):
        return self.request('DELETE', endpoint)
