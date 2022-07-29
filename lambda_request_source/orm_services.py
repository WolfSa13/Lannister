import datetime

import sqlalchemy as db
from sqlalchemy import or_, and_
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import ColumnElement as ColElem
import os

from models import RequestHistory, Request

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

engine = db.create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
metadata = db.MetaData(engine)
db.MetaData.reflect(metadata)

Requests = metadata.tables['requests']
TypeBonuses = metadata.tables['type_bonus']
Users = metadata.tables['users']
Roles = metadata.tables['roles']
UsersRolesRelation = metadata.tables['users_roles_relation']


class RequestQuery:
    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_requests(request_id=None):
        with Session(engine) as session:
            creator = db.orm.aliased(Users)
            reviewer = db.orm.aliased(Users)
            query = session.query(Requests, ColElem.label(TypeBonuses.c.type, 'bonus_name'),
                                  ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(creator.c.slack_id, 'creator_slack_id'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name'),
                                  ColElem.label(reviewer.c.slack_id, 'reviewer_slack_id')).order_by(Requests.columns.id)
            if request_id is not None:
                query = query.filter(Requests.columns.id == request_id)

            query_result = query.join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id).all()

        return query_result

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests/{request_id}'
    #
    # response = requests.patch(url=url, data=data) (data оця з агрументів)
    @staticmethod
    def update_request(request_id, data):
        with Session(engine) as session:
            try:
                query = session.query(Requests).filter(Requests.columns.id == request_id)
                query.update(data)
                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return 1

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests/{request_id}'
    #
    # response = requests.delete(url=url)
    @staticmethod
    def delete_request(request_id):
        with Session(engine) as session:
            try:
                query = session.query(Requests).filter(Requests.columns.id == request_id)
                query_result = query.delete()

                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return query_result

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests'
    #
    # response = requests.post(url=url, data=data) (data оця з агрументів)
    @staticmethod
    def add_new_request(data):
        BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
        url = f'{BASE_URL}/requests'

        response = requests.post(url=url, data=data)

        response.status_code
        response.json()
        # with Session(engine) as session:
        #     try:
        #         new_request = Request(**data)
        #         session.add(new_request)
        #         session.flush()
        #         create_request_id = new_request.id
        #
        #         session.commit()
        #     except db.exc.SQLAlchemyError as e:
        #         session.rollback()
        #         return 0
        #
        # return create_request_id

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests?type=1&status={status}&reviewer_id={reviewer_id}'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_filtered_requests(status, reviewer_id):
        with Session(engine) as session:
            creator = db.orm.aliased(Users)
            reviewer = db.orm.aliased(Users)
            query = session.query(Requests, ColElem.label(TypeBonuses.c.type, 'bonus_name'),
                                  ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(creator.c.slack_id, 'creator_slack_id'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name'),
                                  ColElem.label(reviewer.c.slack_id, 'reviewer_slack_id')).order_by(Requests.columns.id)

            query = query.filter(Requests.columns.status == status)
            query = query.filter(Requests.columns.reviewer == reviewer_id)

            query_result = query.join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id).all()

        return query_result

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests?type=2&creator_id={creator_id}'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_worker_pending_unpaid_requests(creator_id):
        with Session(engine) as session:
            creator = db.orm.aliased(Users)
            reviewer = db.orm.aliased(Users)
            query = session.query(Requests, ColElem.label(TypeBonuses.c.type, 'bonus_name'),
                                  ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(creator.c.slack_id, 'creator_slack_id'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name'),
                                  ColElem.label(reviewer.c.slack_id, 'reviewer_slack_id')).order_by(Requests.columns.id)

            today = datetime.datetime.today()
            today = f'{today.year}-{today.month}-{today.day}'

            query = query.filter(or_(Requests.columns.status == 'created',
                                     and_(Requests.columns.status == 'approved',
                                          Requests.columns.payment_date >= today)))
            query = query.filter(Requests.columns.creator == creator_id)

            query_result = query.join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id).all()

            return query_result

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests?type=3&creator_id={creator_id}'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_worker_approved_denied_requests(creator_id):
        with Session(engine) as session:
            creator = db.orm.aliased(Users)
            reviewer = db.orm.aliased(Users)
            query = session.query(Requests, ColElem.label(TypeBonuses.c.type, 'bonus_name'),
                                  ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(creator.c.slack_id, 'creator_slack_id'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name'),
                                  ColElem.label(reviewer.c.slack_id, 'reviewer_slack_id')).order_by(Requests.columns.id)

            today = datetime.datetime.today()
            today = f'{today.year}-{today.month}-{today.day}'

            query = query.filter(or_(Requests.columns.status == 'denied',
                                     and_(Requests.columns.status == 'approved',
                                          Requests.columns.payment_date < today)))
            query = query.filter(Requests.columns.creator == creator_id)

            query_result = query.join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id).all()

            return query_result

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests?type=4&creator_id={creator_id}'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_worker_deleted_requests(creator_id):
        with Session(engine) as session:
            creator = db.orm.aliased(Users)
            reviewer = db.orm.aliased(Users)
            query = session.query(Requests, ColElem.label(TypeBonuses.c.type, 'bonus_name'),
                                  ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(creator.c.slack_id, 'creator_slack_id'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name'),
                                  ColElem.label(reviewer.c.slack_id, 'reviewer_slack_id')).order_by(Requests.columns.id)

            query = query.filter(Requests.columns.status == 'deleted')
            query = query.filter(Requests.columns.creator == creator_id)

            query_result = query.join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id).all()

            return query_result

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests?type=5&query_name={query_name}'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_administrator_all_requests(query_name):
        with Session(engine) as session:
            creator = db.orm.aliased(Users)
            reviewer = db.orm.aliased(Users)
            query = session.query(Requests, ColElem.label(TypeBonuses.c.type, 'bonus_name'),
                                  ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(creator.c.slack_id, 'creator_slack_id'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name'),
                                  ColElem.label(reviewer.c.slack_id, 'reviewer_slack_id')).order_by(Requests.columns.id)

            if query_name == 'pending':
                query = query.filter(Requests.columns.status == 'created')
            elif query_name == 'unpaid':
                today = datetime.datetime.today()
                today = f'{today.year}-{today.month}-{today.day}'

                query = query.filter(and_(Requests.columns.status == 'approved',
                                          Requests.columns.payment_date >= today))
            elif query_name == 'paid':
                today = datetime.datetime.today()
                today = f'{today.year}-{today.month}-{today.day}'

                query = query.filter(and_(Requests.columns.status == 'approved',
                                          Requests.columns.payment_date < today))
            elif query_name == 'denied':
                query = query.filter(Requests.columns.status == 'denied')
            elif query_name == 'deleted':
                query = query.filter(Requests.columns.status == 'deleted')

            query_result = query.join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id).all()

            return query_result


class UsersQuery:
    @staticmethod
    def get_users(user_id=None, slack_id=None):
        with Session(engine) as session:
            query = session.query(Users, UsersRolesRelation.c.user_id, UsersRolesRelation.c.role_id,
                                  Roles.c.role_name)

            if user_id is not None:
                query = query.filter(Users.c.id == user_id)
            if slack_id is not None:
                query = query.filter(Users.c.slack_id == slack_id)

            query = query.join(UsersRolesRelation, Users.c.id == UsersRolesRelation.c.user_id) \
                .join(Roles, UsersRolesRelation.c.role_id == Roles.c.id)

            query_result = query.all()

        return UsersQuery._parse_users_data(query_result)

    @staticmethod
    def get_user_by_id(user_id):
        user = UsersQuery.get_users(user_id=user_id)[0]
        return user

    @staticmethod
    def get_user_by_slack_id(slack_id):
        user = UsersQuery.get_users(slack_id=slack_id)[0]
        return user

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/workers?role=reviewer'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_reviewers():
        with Session(engine) as session:
            reviewers = session.query(Roles).filter(Roles.c.role_name == 'reviewer').subquery()
            query = session.query(Users, UsersRolesRelation.c.user_id, UsersRolesRelation.c.role_id,
                                  reviewers.c.role_name) \
                .join(UsersRolesRelation, Users.c.id == UsersRolesRelation.c.user_id) \
                .join(reviewers, UsersRolesRelation.c.role_id == reviewers.c.id)

            query_result = query.all()

        return UsersQuery._parse_users_data(query_result)

    @staticmethod
    def _parse_users_data(users_data):
        parsed_result = dict()
        for item in users_data:
            if item['id'] not in parsed_result:
                parsed_result[item['id']] = {
                    'id': item['id'],
                    'full_name': item['full_name'],
                    'position': item['position'],
                    'slack_id': item['slack_id'],
                    'roles': [item['role_name']]
                }
            else:
                parsed_result[item['id']]['roles'].append(item['role_name'])

        return list(parsed_result.values())


class TypeBonusesQuery:
    # ці вже є в папці бонусів
    @staticmethod
    def get_bonuses(bonus_id=None):
        with Session(engine) as session:
            query = session.query(TypeBonuses).order_by(TypeBonuses.c.id)

            if bonus_id is not None:
                query = query.filter(TypeBonuses.c.id == bonus_id)

            query_result = query.all()

        return TypeBonusesQuery._parse_bonuses_data(query_result)

    @staticmethod
    def _parse_bonuses_data(bonuses_data):
        parsed_result = list()
        for item in bonuses_data:
            parsed_result.append(dict(item))

        return parsed_result


class RequestHistoryQuery:
    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests/{request_id}/history'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_request_history(request_id):
        with Session(engine) as session:
            query = session.query(RequestHistory).filter(RequestHistory.request_id == request_id)

            query_result = query.all()

        return query_result

    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests/{request_id}/history'
    #
    # response = requests.post(url=url)
    # але тут вже зі мною треба фіксати
    @staticmethod
    def add_history(data, request_id, editor, old_request=None):
        with Session(engine) as session:
            try:
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

                new_history = RequestHistory(request_id=request_id, changes=changes_log, editor=editor)
                session.add(new_history)

                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0
        return 1
