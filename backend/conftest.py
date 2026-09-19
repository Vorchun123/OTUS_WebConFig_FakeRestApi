import pytest
from backend.page.authors import Authors
from backend.page.books import Books
from backend.page.users import Users


@pytest.fixture
def authors_client():
    return Authors()


@pytest.fixture
def books_client():
    return Books()


@pytest.fixture
def user_client():
    return Users()
