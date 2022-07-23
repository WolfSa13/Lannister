import sqlalchemy as db
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import ColumnElement as ColElem
import os

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
    @staticmethod
    def get_requests(request_id=None):
        with Session(engine) as session:
            creator = db.orm.aliased(Users)
            reviewer = db.orm.aliased(Users)
            query = session.query(Requests, ColElem.label(TypeBonuses.c.type, 'bonus_name'),
                                  ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name')).order_by(Requests.columns.id)
            if request_id is not None:
                query = query.filter(Requests.columns.id == request_id)

            query_result = query.join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id).all()

        return query_result

    @staticmethod
    def update_request(request_id, data):
        with Session(engine) as session:
            query = session.query(Requests).filter(Requests.columns.id == request_id)
            query_result = query.update(data)

            session.commit()

        return query_result

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

    @staticmethod
    def add_new_request(data):
        with Session(engine) as session:
            try:
                insert = Requests.insert() \
                    .values(creator=data['creator'], reviewer=data['reviewer'], status='created',
                            type_bonus=data['type_bonus'],
                            payment_amount=data['payment_amount'], description=data['description'])

                session.execute(insert)
                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return 1

    @staticmethod
    def get_filtered_requests(status=None, reviewer_id=None, creator_id=None, payment_date=None):
        with Session(engine) as session:
            creator = db.orm.aliased(Users, 'creator')
            reviewer = db.orm.aliased(Users, 'reviewer')
            query = session.query(Requests, TypeBonuses, ColElem.label(creator.c.full_name, 'creator_name'),
                                  ColElem.label(creator.c.slack_id, 'creator_slack_id'),
                                  ColElem.label(reviewer.c.full_name, 'reviewer_name'),
                                  ColElem.label(reviewer.c.slack_id, 'reviewer_slack_id')) \
                .join(TypeBonuses, Requests.c.type_bonus == TypeBonuses.c.id) \
                .join(creator, Requests.c.creator == creator.c.id) \
                .join(reviewer, Requests.c.reviewer == reviewer.c.id)

            if status is not None:
                query = query.filter(Requests.c.status == status)
            if payment_date is not None:
                query = query.filter(Requests.c.payment_date == payment_date)
            if reviewer_id is not None:
                query = query.filter(reviewer.c.slack_id == reviewer_id)
            if creator_id is not None:
                query = query.filter(creator.c.slack_id == creator_id)

            query_result = query.all()

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

        return  parsed_result
