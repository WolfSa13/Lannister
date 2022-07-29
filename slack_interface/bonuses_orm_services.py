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

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/bonuses/{bonus_id}'
    #
    # response = requests.patch(url=url, data=data) (data це оця що приходить в метод параметром)
    @staticmethod
    def update_bonuses(bonus_id, data):
        url = f'{URL}/{bonus_id}'

        response = requests.patch(url=url, data=data)

        if response.status_code == 200:
            return response.json()

        return None

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/bonuses/{bonus_id}'
    #
    # response = requests.delete(url=url)
    @staticmethod
    def delete_bonuses(bonus_id):
        with Session(engine) as session:
            try:
                query = session.query(TypeBonuses).filter(
                    TypeBonuses.columns.id == bonus_id)
                query.delete()

                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return 1

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/bonuses/{bonus_id}'
    #
    # response = requests.post(url=url, data=data) (data це оця що приходить в метод параметром)
    @staticmethod
    def add_new_bonus(data):
        response = requests.post(url=URL, data=data)

        if response.status_code == 201:
            return response.json()

        return None

#
# class UsersQuery:
#     # import requests
#     #
#     # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
#     # url = f'{BASE_URL}/workers'
#     #
#     # response = requests.get(url=url)
#     @staticmethod
#     def get_users(user_id=None, slack_id=None):
#         with Session(engine) as session:
#             query = session.query(Users, UsersRolesRelation.c.user_id, UsersRolesRelation.c.role_id,
#                                   Roles.c.role_name)
#
#             if user_id is not None:
#                 query = query.filter(Users.c.id == user_id)
#             if slack_id is not None:
#                 query = query.filter(Users.c.slack_id == slack_id)
#
#             query = query.join(UsersRolesRelation, Users.c.id == UsersRolesRelation.c.user_id) \
#                 .join(Roles, UsersRolesRelation.c.role_id == Roles.c.id)
#
#             query_result = query.all()
#
#         return UsersQuery._parse_users_data(query_result)
#
#     # import requests
#     #
#     # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
#     # url = f'{BASE_URL}/workers?slack_id={slack_id}'
#     #
#     # response = requests.get(url=url)
#     @staticmethod
#     def get_user_by_slack_id(slack_id):
#         user = UsersQuery.get_users(slack_id=slack_id)[0]
#         return user
#
#     @staticmethod
#     def _parse_users_data(users_data):
#         parsed_result = dict()
#         for item in users_data:
#             if item['id'] not in parsed_result:
#                 parsed_result[item['id']] = {
#                     'id': item['id'],
#                     'full_name': item['full_name'],
#                     'position': item['position'],
#                     'slack_id': item['slack_id'],
#                     'roles': [item['role_name']]
#                 }
#             else:
#                 parsed_result[item['id']]['roles'].append(item['role_name'])
#
#         return list(parsed_result.values())
