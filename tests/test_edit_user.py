import allure
import pytest
from helpers.helpers import *

class TestEditUser:

    @allure.title('Изменение пользовательских данных, status_code = 200')
    @pytest.mark.parametrize(
        "new_email,new_password,new_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_edit_authorized_user(self, new_email, new_password, new_name):
        credentials = user_generate_login()
        user_register(credentials)
        auth_response = user_authorization(credentials)
        user = auth_response.json()['user']
        new_credentials = user_generate_login()
        if new_email:
            user['email'] = new_credentials['email']
        if new_password:
            user['password'] = new_credentials['password']
        if new_name:
            user['name'] = new_credentials['name']
        edit_response = user_edit(user, {'Authorization': auth_response.json()['accessToken']})
        assert edit_response.status_code == 200
        assert edit_response.json()['success'] is True
        assert edit_response.json()['user']['email'] == user['email']
        assert edit_response.json()['user']['name'] == user['name']

    @allure.title('Изменение email на уже созданный, status_code = 403, сообщение об ошибке')
    def test_edit_authorized_used_with_used_email(self):
        credentials_1 = user_generate_login()
        user_register(credentials_1)  # Регистрируем пользователя #1
        credentials_2 = user_generate_login()
        user_register(credentials_2)  # Регистрируем пользователя #2
        auth_response = user_authorization(credentials_2)  # Авторизуем пользователя #2
        user = auth_response.json()['user']  # Получаем текущие данные
        user['email'] = credentials_1['email']  # Меняем почту на почту пользователя #1
        edit_response = user_edit(user, {'Authorization': auth_response.json()['accessToken']})
        assert edit_response.status_code == 403
        assert edit_response.json()['message'] == 'User with such email already exists'

    @allure.title('Изменение пользовательских данных без авторизации, status_code = 401, сообщение об ошибке')
    @pytest.mark.parametrize(
        "new_email,new_password,new_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_edit_not_authorized_user(self, new_email, new_password, new_name):
        credentials = user_generate_login()
        register_response = user_register(credentials)
        user = register_response.json()['user']
        new_credentials = user_generate_login()
        if new_email:
            user['email'] = new_credentials['email']
        if new_password:
            user['password'] = new_credentials['password']
        if new_name:
            user['name'] = new_credentials['name']
        edit_response = user_edit(user)
        assert edit_response.status_code == 401
        assert edit_response.json()['message'] == 'You should be authorised'

