import pytest
import allure


@pytest.mark.api
@allure.title('Проверяем информацию о количестве пользователей')
def test_get_users(user_client):
    result = user_client.get_users()
    assert len(result) == 10


@pytest.mark.api
@allure.title('Проверяем информацию о пользователе по id')
@pytest.mark.parametrize('user_id, user_name, password',
                         [(4, 'User 4', 'Password4'),
                          (6, 'User 6', 'Password6')])
def test_get_user_by_id(user_client, user_id, user_name, password):
    result = user_client.get_user_by_id(user_id)
    assert result['id'] == user_id
    assert result['userName'] == user_name
    assert result['password'] == password


@pytest.mark.api
@allure.title('Добавляем нового пользователя')
@pytest.mark.parametrize('user_id, user_name, password',
                         [(12, 'Pipker', 'asdQWEfg56'),
                          (34, 'somebody', 'WQE435!@fd')])
def test_create_user(user_client, user_id, user_name, password):
    result = user_client.add_new_user(user_id, user_name, password)
    assert result.get('id') == user_id
    assert result.get('userName') == user_name
    assert result.get('password') == password


@pytest.mark.api
@allure.title('Изменяем параметры пользователя')
@pytest.mark.parametrize('user_id, user_name, password',
                         [(4, 'Mr.D', '^&sdfew32'),
                          (7, 'Ms.G', '&^*dfgqw1')])
def test_change_user(user_client, user_id, user_name, password):
    result = user_client.change_user(user_id, user_name, password)
    assert result.get('id') == user_id
    assert result.get('userName') == user_name
    assert result.get('password') == password


@pytest.mark.api
@allure.title('Удаляем пользователя')
@pytest.mark.parametrize('user_id', [4, 8])
def test_delete_user(user_client, user_id):
    result = user_client.delete_user(user_id)
    assert result is None
