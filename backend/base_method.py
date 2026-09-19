import requests


class BaseMethod:
    def method_get(self, url):
        response = requests.get(url)
        response.raise_for_status()
        result = response.json()
        return result

    def method_get_with_id(self, url, id):
        response = requests.get(f'{url}/{id}')
        response.raise_for_status()
        result = response.json()
        return result

    def method_post(self, url, body):
        response = requests.post(url, json=body)
        response.raise_for_status()
        result = response.json()
        return result

    def method_put(self, url, body, id):
        response = requests.put(f'{url}/{id}', json=body)
        response.raise_for_status()
        result = response.json()
        return result

    def method_delete(self, url, id):
        response = requests.delete(f'{url}/{id}')
        response.raise_for_status()
