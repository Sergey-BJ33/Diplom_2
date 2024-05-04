import allure
from helpers.helpers import *

class TestCreateOrder:

    @allure.title('Создание заказа с ингредиентами, status_code = 200')
    def test_create_order_with_ingredients_with_auth(self):
        credentials = user_generate_login()
        user_register(credentials)
        auth_response = user_authorization(credentials)
        ingredients_hashes = get_ingredients_hashes()
        response = order_create(ingredients_hashes, {'Authorization': auth_response.json()['accessToken']})
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'name' in response.json()
        assert 'order' in response.json()
        assert 'number' in response.json()['order']
        assert 'ingredients' in response.json()['order']
        hashes = [ingredient['_id'] for ingredient in response.json()['order']['ingredients']]
        for ingredient_hash in ingredients_hashes:
            assert ingredient_hash in hashes

    @allure.title('Создание не авторизованного заказа с ингредиентами, status_code = 200')
    def test_create_order_with_ingredients_without_auth(self):
        ingredients_hashes = get_ingredients_hashes()
        response = order_create(ingredients_hashes)
        assert response.status_code == 200
        assert response.json()['success'] is True
        assert 'name' in response.json()
        assert 'order' in response.json()
        assert 'number' in response.json()['order']

    @allure.title('Создание заказа без ингредиентов, status_code = 400, сообщение об ошибке')
    def test_create_order_without_ingredients_with_auth(self):
        credentials = user_generate_login()
        user_register(credentials)
        auth_response = user_authorization(credentials)
        response = order_create([], {'Authorization': auth_response.json()['accessToken']})
        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание заказа с несуществующими ингредиентами, status_code = 500')
    def test_create_order_with_invalid_ingredients_hash_with_auth(self):
        credentials = user_generate_login()
        user_register(credentials)
        auth_response = user_authorization(credentials)
        ingredients_hashes = ['this-is-invalid-hash']
        response = order_create(ingredients_hashes, {'Authorization': auth_response.json()['accessToken']})
        assert response.status_code == 500

    @allure.title('Создание не авторизованного заказа без ингредиентов, status_code = 400, сообщение об ошибке')
    def test_create_order_without_ingredients_without_auth(self):
        response = order_create([])
        assert response.status_code == 400
        assert response.json()['success'] is False
        assert response.json()['message'] == 'Ingredient ids must be provided'

    @allure.title('Создание не авторизованного заказа с несуществующими ингредиентами, status_code = 500')
    def test_create_order_with_invalid_ingredients_hash_without_auth(self):
        ingredients_hashes = ['this-is-invalid-hash']
        response = order_create(ingredients_hashes)
        assert response.status_code == 500
