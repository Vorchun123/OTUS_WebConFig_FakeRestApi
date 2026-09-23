from backend.base_method import BaseMethod
import allure


class Books(BaseMethod):
    ENDPOINT = '/Books'

    @allure.step('Получаем список всех книг')
    def get_books(self):
        return self.method_get(self.ENDPOINT)

    @allure.step('Получаем информацию о книге по id')
    def get_book_by_id(self, book_id):
        return self.method_get(f'{self.ENDPOINT}/{book_id}')

    @allure.step('Добавляем новую книгу с параметрами')
    def add_new_book(self, book_id, title, description, page_count, excerpt, publish_date):
        body = {'id': book_id,
                'title': title,
                'description': description,
                'pageCount': page_count,
                'excerpt': excerpt,
                'publishDate': publish_date}
        return self.method_post(self.ENDPOINT, body)

    @allure.step('Меняем параметры книги по id')
    def change_book(self, book_id, title, description, page_count, excerpt, publish_date):
        body = {'id': book_id,
                'title': title,
                'description': description,
                'pageCount': page_count,
                'excerpt': excerpt,
                'publishDate': publish_date}
        return self.method_put(f'{self.ENDPOINT}/{book_id}', body)

    @allure.step('Удаляем книгу по id')
    def delete_book(self, book_id):
        return self.method_delete(f'{self.ENDPOINT}/{book_id}')
