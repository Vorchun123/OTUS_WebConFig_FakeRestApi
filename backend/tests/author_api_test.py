import pytest


@pytest.mark.api
def test_get_author(authors_client):
    result = authors_client.get_authors()
    assert len(result) > 560


@pytest.mark.api
@pytest.mark.parametrize('author_id, book_id_min, book_id_max',
                         [(4, 1, 2),
                          (47, 14, 19)])
def test_get_author_by_id(authors_client, author_id, book_id_min, book_id_max):
    result = authors_client.get_authors_by_id(author_id)
    assert result['id'] == author_id
    assert book_id_min <= result['idBook'] <= book_id_max
    assert result['firstName'] == f'First Name {author_id}'
    assert result['lastName'] == f'Last Name {author_id}'


@pytest.mark.api
@pytest.mark.parametrize('book_id, count_min, count_max',
                         [(12, 2, 4),
                          (109, 2, 4)])
def test_get_author_by_book_id(authors_client, book_id, count_min, count_max):
    result = authors_client.get_author_by_book_id(book_id)
    assert count_min <= len(result) <= count_max


@pytest.mark.api
@pytest.mark.parametrize('author_id, book_id, firstname, lastname',
                         [(999, 45, 'Pedro', 'Dunkan'),
                          (823, 75, 'Bart', 'Simpson')])
def test_create_author(authors_client, author_id, book_id, firstname, lastname):
    result = authors_client.add_new_author(author_id, book_id, firstname, lastname)
    assert result.get('id') == author_id
    assert result.get('idBook') == book_id
    assert result.get('firstName') == firstname
    assert result.get('lastName') == lastname


@pytest.mark.api
@pytest.mark.parametrize('author_id', [34, 93])
def test_delete_author(authors_client, author_id):
    result = authors_client.delete_author(author_id)
    assert result is None
