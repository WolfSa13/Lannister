import datetime
import requests
import os

# BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
BASE_URL = os.environ.get('BASE_URL')
URL = f'{BASE_URL}/requests'


class RequestQuery:
    @staticmethod
    def get_requests(request_id=None):
        url = URL

        if request_id is not None:
            url += f'/{request_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def update_request(request_id, data):
        url = f'{URL}/{request_id}'

        response = requests.patch(url=url, data=data)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def delete_request(request_id):
        url = f'{URL}/{request_id}'

        response = requests.patch(url=url)

        if response.status_code == 204:
            return 1

        return None

    @staticmethod
    def add_new_request(data):
        response = requests.post(url=URL, data=data)

        if response.status_code == 201:
            return response.json()

        return None

    @staticmethod
    def get_filtered_requests(status, reviewer_id):
        url = f'{URL}?type=1&status={status}&reviewer_id={reviewer_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def get_worker_pending_unpaid_requests(creator_id):
        url = f'{URL}?type=2&creator_id={creator_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def get_worker_approved_denied_requests(creator_id):
        url = f'{URL}?type=3&creator_id={creator_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def get_worker_deleted_requests(creator_id):
        url = f'{URL}?type=4&creator_id={creator_id}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests?type=5&query_name={query_name}'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_administrator_all_requests(query_name):
        url = f'{URL}?type=5&query_name={query_name}'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None


class RequestHistoryQuery:
    @staticmethod
    def get_request_history(request_id):
        url = f'{URL}/{request_id}/history'

        response = requests.get(url=url)

        if response.status_code == 200:
            return response.json()

        return None

    @staticmethod
    def add_history(data, request_id, editor, old_request=None):
        if old_request is not None:
            request = dict(old_request)
        else:
            request = dict()

        changes_log = ''
        for key in data.keys():
            if str(data[key]) != str(request.get(key, "-")):
                if key == 'reviewer' or key == 'type_bonus' or key == 'creator':
                    continue

                log = f'{" ".join(key.split("_")).capitalize()}:  {request.get(key, "-")}  ->  {data[key]}\n'
                changes_log += log

        new_history = {
            'request_id': request_id,
            'changes': changes_log,
            'editor': editor
        }

        url = f'{URL}/{request_id}/history'

        response = requests.post(url=url, data=new_history)

        if response.status_code == 201:
            return response.json()

        return None
