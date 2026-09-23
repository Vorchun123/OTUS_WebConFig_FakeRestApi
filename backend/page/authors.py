from backend.base_method import BaseMethod
import allure


class Authors(BaseMethod):
    ENDPOINT = '/Authors'
    ENDPOINT_BY_BOOKS = '/Authors/authors/books'

    @allure.step('Получаем список всех авторов')
    def get_authors(self):
        return self.method_get(self.ENDPOINT)

    @allure.step('Получаем информацию об авторе по id')
    def get_authors_by_id(self, author_id):
        return self.method_get(f'{self.ENDPOINT}/{author_id}')

    @allure.step('Получаем информацию об авторе по id книги')
    def get_author_by_book_id(self, book_id):
        return self.method_get(f'{self.ENDPOINT_BY_BOOKS}/{book_id}')

    @allure.step('Добавляем нового авторе с параметрами')
    def add_new_author(self, author_id, book_id, firstname, lastname):
        body = {'id': author_id,
                'idBook': book_id,
                'firstName': firstname,
                'lastName': lastname}
        return self.method_post(self.ENDPOINT, body)

    @allure.step('Удаляем автора по id')
    def delete_author(self, author_id):
        return self.method_delete(f'{self.ENDPOINT}/{author_id}')
