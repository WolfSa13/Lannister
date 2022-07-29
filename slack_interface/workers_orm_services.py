import os
import requests

# BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
BASE_URL = os.environ.get('BASE_URL')
URL = f'{BASE_URL}/workers'


class UsersQuery:
    @staticmethod
    def get_users():
        url = URL

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_user_by_id(user_id):
        url = f'{BASE_URL}/workers/{user_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

    @staticmethod
    def get_user_by_slack_id(slack_id):
        url = f'{URL}?slack_id={slack_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def update_user(user_id, data):
        url = f'{URL}/{user_id}'

        print(url)
        print(data)

        response = requests.patch(url=url, json=data)

        print(response.status_code)
        print(response.json())

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def delete_user(user_id):
        url = f'{URL}/{user_id}'

        response = requests.delete(url=url)

        if response.status_code == 204:
            return 1

        return None

    @staticmethod
    def add_new_user(data):
        print(data)

        response = requests.post(url=URL, json=data)

        print(response.status_code)
        print(response.json())

        if response.status_code == 201:
            return response.json()

        return None

    @staticmethod
    def get_reviewers():
        url = f'{URL}?role=reviewer'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()
