import os
import requests

# BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
BASE_URL = os.environ.get('BASE_URL')
URL = f'{BASE_URL}/bonuses'


class TypeBonusesQuery:
    @staticmethod
    def get_bonuses(bonus_id=None):
        url = URL

        if bonus_id is not None:
            url += f'/{bonus_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def update_bonuses(bonus_id, data):
        url = f'{URL}/{bonus_id}'

        response = requests.patch(url=url, json=data)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def delete_bonuses(bonus_id):
        url = f'{URL}/{bonus_id}'

        response = requests.delete(url=url)

        if response.status_code == 204:
            return 1

        return None

    @staticmethod
    def add_new_bonus(data):
        response = requests.post(url=URL, json=data)

        if response.status_code == 201:
            return response.json()

        return None

