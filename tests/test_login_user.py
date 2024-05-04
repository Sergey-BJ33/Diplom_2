import allure
from helpers.helpers import *

class TestLoginUser:

    @allure.title('Авторизация пользователя, status_code = 200')
    def test_login_registered_user(self):
        credentials = user_generate_login()
        user_register(credentials)
        response = user_authorization(credentials)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert response.json()['user']['email'] == credentials['email']
        assert response.json()['user']['name'] == credentials['name']
        assert 'accessToken' in response.json()
        assert 'refreshToken' in response.json()

    @allure.title('Авторизация незарегистрированного пользователя, status_code = 401, сообщение об ошибке')
    def test_login_not_registered_user(self):
        credentials = user_generate_login(exclude_name=True)
        response = user_authorization(credentials)
        assert response.status_code == 401
        assert response.json()['success'] is False
        assert response.json()['message'] == "email or password are incorrect"
