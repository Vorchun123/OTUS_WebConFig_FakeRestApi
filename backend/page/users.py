from backend.base_method import BaseMethod


class Users(BaseMethod):
    URL = 'https://fakerestapi.azurewebsites.net/api/v1/Users'

    def get_users(self):
        return self.method_get(self.URL)

    def get_user_by_id(self, user_id):
        return self.method_get_with_id(self.URL, user_id)

    def add_new_user(self, user_id, user_name, password):
        body = {'id': user_id,
                'userName': user_name,
                'password': password}
        return self.method_post(self.URL, body)

    def change_user(self, user_id, user_name, password):
        body = {'id': user_id,
                'userName': user_name,
                'password': password}
        return self.method_put(self.URL, body, user_id)

    def delete_user(self, user_id):
        return self.method_delete(self.URL, user_id)