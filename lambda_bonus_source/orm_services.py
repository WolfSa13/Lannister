import sqlalchemy as db
from sqlalchemy.orm.session import Session
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

TypeBonuses = metadata.tables['type_bonus']
Users = metadata.tables['users']
Roles = metadata.tables['roles']
UsersRolesRelation = metadata.tables['users_roles_relation']


class TypeBonusesQuery:

    @staticmethod
    def get_bonuses(bonus_id=None):
        with Session(engine) as session:
            query = session.query(TypeBonuses).order_by(TypeBonuses.columns.id)

            if bonus_id is not None:
                query = query.filter(TypeBonuses.columns.id == bonus_id)

            query_result = query.all()

        return query_result

    @staticmethod
    def update_bonuses(bonus_id, data):
        with Session(engine) as session:
            try:
                query = session.query(TypeBonuses).filter(
                    TypeBonuses.columns.id == bonus_id)
                query.update(data)

                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return 1

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

    @staticmethod
    def add_new_bonus(data):
        with Session(engine) as session:
            try:
                insert = TypeBonuses.insert().values(type=data['type'], description=data['description'])
                session.execute(insert)
                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return 1


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
    def get_user_by_slack_id(slack_id):
        user = UsersQuery.get_users(slack_id=slack_id)[0]
        return user

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
