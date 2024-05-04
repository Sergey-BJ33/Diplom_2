import allure
import pytest
from helpers.helpers import *


class TestCreateUser:

    @allure.title('Успешная регистрация уникального пользователя, status_code = 200')
    def test_create_unique_user(self):
        credentials = user_generate_login()
        response = user_register(credentials)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == credentials['email']
        assert response.json()['user']['name'] == credentials['name']
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

    @allure.title('Регистрация пользователя без заполнения обязательного поля, status_code = 403, сообщение об ошибке')
    @pytest.mark.parametrize(
        "exclude_email,exclude_password,exclude_name",
        [
            [True, False, False],
            [False, True, False],
            [False, False, True],
        ]
    )
    def test_create_user_without_required_field(self, exclude_email, exclude_password, exclude_name):
        credentials = user_generate_login(exclude_email, exclude_password, exclude_name)
        response = user_register(credentials)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Email, password and name are required fields'

    @allure.title('Создание пользователя, который уже зарегистрирован, status_code = 403, сообщение об ошибке')
    def test_create_already_existing_user(self):
        credentials = user_generate_login()
        user_register(credentials)
        response = user_register(credentials)
        assert response.status_code == 403
        assert response.json()['success'] is False
        assert response.json()['message'] == 'User already exists'