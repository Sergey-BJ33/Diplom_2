import allure
import random
import requests
import string
from data import *


@allure.step('Получить список хэшей ингредиентов')
def get_ingredients_hashes() -> list:
    ingredients_response = requests.get(ingredients)
    return [ingredient['_id'] for ingredient in ingredients_response.json()['data']]

@allure.step('Создать заказ')
def order_create(ingredients_hashes, headers=None) -> requests.Response:
    if headers:
        return requests.post(orders, {'ingredients': ingredients_hashes}, headers=headers)
    else:
        return requests.post(orders, {'ingredients': ingredients_hashes})

@allure.step('Получить список заказов пользователя')
def orders_get(headers=None):
    if headers:
        return requests.get(orders, headers=headers)
    else:
        return requests.get(orders)

@allure.step('Получить список всех заказов')
def get_all_orders():
    return requests.get(orders_all)

@allure.step('Сгенерировать учётные данные пользоваться')
def user_generate_login(exclude_email=False, exclude_password=False, exclude_name=False) -> dict:
    def generate_random_string(length):
        letters = string.ascii_lowercase
        random_string = ''.join(random.choice(letters) for _ in range(length))
        return random_string
    credentials = {}
    if not exclude_email:
        credentials['email'] = generate_random_string(8) + '@ya.ru'
    if not exclude_password:
        credentials['password'] = generate_random_string(12)
    if not exclude_name:
        credentials['name'] = generate_random_string(8)
    return credentials

@allure.step('Регистрация пользователя')
def user_register(credentials) -> requests.Response:
    return requests.post(register_auth, json=credentials)

@allure.step('Авторизация пользователя')
def user_authorization(credentials) -> requests.Response:
    return requests.post(login_auth, json=credentials)

@allure.step('Редактировать данные пользователя')
def user_edit(user, headers=None) -> requests.Response:
    if headers:
        return requests.patch(user_auth, user, headers=headers)
    else:
        return requests.patch(user_auth, user)
