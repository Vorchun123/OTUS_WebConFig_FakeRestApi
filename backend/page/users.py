from backend.base_method import BaseMethod
import allure


class Users(BaseMethod):
    ENDPOINT = '/Users'

    @allure.step('Получаем список всех пользователей')
    def get_users(self):
        return self.method_get(self.ENDPOINT)

    @allure.step('Получаем информацию о пользователе по id')
    def get_user_by_id(self, user_id):
        return self.method_get(f'{self.ENDPOINT}/{user_id}')

    @allure.step('Добавляем нового пользователя с параметрами')
    def add_new_user(self, user_id, user_name, password):
        body = {'id': user_id,
                'userName': user_name,
                'password': password}
        return self.method_post(self.ENDPOINT, body)

    @allure.step('Меняем параметры пользователя по id')
    def change_user(self, user_id, user_name, password):
        body = {'id': user_id,
                'userName': user_name,
                'password': password}
        return self.method_put(f'{self.ENDPOINT}/{user_id}', body)

    @allure.step('Удаляем пользователя по id')
    def delete_user(self, user_id):
        return self.method_delete(f'{self.ENDPOINT}/{user_id}')
