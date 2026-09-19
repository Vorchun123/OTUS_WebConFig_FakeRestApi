from backend.base_method import BaseMethod


class Books(BaseMethod):
    URL = 'https://fakerestapi.azurewebsites.net/api/v1/Books'

    def get_books(self):
        return self.method_get(self.URL)

    def get_book_by_id(self, book_id):
        return self.method_get_with_id(self.URL, book_id)

    def add_new_book(self, book_id, title, description, page_count, excerpt, publish_date):
        body = {'id': book_id,
                'title': title,
                'description': description,
                'pageCount': page_count,
                'excerpt': excerpt,
                'publishDate': publish_date}
        return self.method_post(self.URL, body)

    def change_book(self, book_id, title, description, page_count, excerpt, publish_date):
        body = {'id': book_id,
                'title': title,
                'description': description,
                'pageCount': page_count,
                'excerpt': excerpt,
                'publishDate': publish_date}
        return self.method_put(self.URL, body, book_id)

    def delete_book(self, book_id):
        return self.method_delete(self.URL, book_id)