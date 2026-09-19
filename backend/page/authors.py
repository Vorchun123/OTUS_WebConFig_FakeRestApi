from backend.base_method import BaseMethod


class Authors(BaseMethod):
    URL = 'https://fakerestapi.azurewebsites.net/api/v1/Authors'
    URL_BOOKS_ID = 'https://fakerestapi.azurewebsites.net/api/v1/Authors/authors/books'

    def get_authors(self):
        return self.method_get(self.URL)

    def get_authors_by_id(self, author_id):
        return self.method_get_with_id(self.URL, author_id)

    def get_author_by_book_id(self, book_id):
        return self.method_get_with_id(self.URL_BOOKS_ID, book_id)

    def add_new_author(self, author_id, book_id, firstname, lastname):
        body = {'id': author_id,
                'idBook': book_id,
                'firstName': firstname,
                'lastName': lastname}
        return self.method_post(self.URL, body)

    def delete_author(self, author_id):
        return self.method_delete(self.URL, author_id)
