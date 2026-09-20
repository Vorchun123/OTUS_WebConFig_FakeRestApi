import pytest


@pytest.mark.api
def test_get_books(books_client):
    result = books_client.get_books()
    assert len(result) == 200


@pytest.mark.api
@pytest.mark.parametrize('book_id, title, page_count',
                         [(45, 'Book 45', 4500),
                          (163, 'Book 163', 16300)])
def test_get_book_by_id(books_client, book_id, title, page_count):
    result = books_client.get_book_by_id(book_id)
    assert result['id'] == book_id
    assert result['title'] == title
    assert result['pageCount'] == page_count


@pytest.mark.api
@pytest.mark.parametrize('book_id, title, description, page_count, excerpt, publish_date',
                         [(345, 'New book', 'a story about nothing', 258, 'nothing nothing nothing',
                           '2026-12-01T00:12:45'),
                          (612, 'The story of the fox', 'the life of a fox', 39, 'Once upon a time, there was a fox',
                           '2024-08-27T02:45:34')])
def test_create_book(books_client, book_id, title, description, page_count, excerpt, publish_date):
    result = books_client.add_new_book(book_id, title, description, page_count, excerpt, publish_date)
    assert result.get('id') == book_id
    assert result.get('title') == title
    assert result.get('description') == description
    assert result.get('pageCount') == page_count


@pytest.mark.api
@pytest.mark.parametrize('book_id, title, description, page_count, excerpt, publish_date',
                         [(145, 'New book', 'a story about nothing', 28, 'nothing nothing nothing',
                           '2026-12-01T00:12:45'),
                          (12, 'The story of the fox', 'the life of a fox', 397, 'Once upon a time, there was a fox',
                           '2024-08-27T02:45:34')])
def test_change_book(books_client, book_id, title, description, page_count, excerpt, publish_date):
    result = books_client.change_book(book_id, title, description, page_count, excerpt, publish_date)
    assert result.get('id') == book_id
    assert result.get('title') == title
    assert result.get('description') == description
    assert result.get('pageCount') == page_count


@pytest.mark.api
@pytest.mark.parametrize('book_id', [54, 193])
def test_delete_book(books_client, book_id):
    result = books_client.delete_book(book_id)
    assert result is None
