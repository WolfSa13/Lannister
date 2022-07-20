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

Requests = metadata.tables['requests']
TypeBonuses = metadata.tables['type_bonus']
Users = metadata.tables['users']
Roles = metadata.tables['roles']
UsersRolesRelation = metadata.tables['users_roles_relation']


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
        return UsersQuery._parsed_users(query_result)

    @staticmethod
    def _parsed_users(users_data):
        parsed_result = {}
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

    @staticmethod
    def get_user_by_id(user_id):
        user = UsersQuery.get_users(user_id=user_id)[0]
        return user

    @staticmethod
    def get_user_by_slack_id(slack_id):
        user = UsersQuery.get_users(slack_id=slack_id)[0]
        return user

    @staticmethod
    def update_user(user_id, data):
        with Session(engine) as session:
            user = UsersQuery.get_user_by_id(user_id)
            roles_data = data.pop('roles', None)
            if roles_data is not None and roles_data != user['roles']:
                user_roles = session.query(UsersRolesRelation).filter(UsersRolesRelation.c.user_id == user_id).all()
                for user_role in user_roles:
                    if user_role['role_id'] not in roles_data:
                        session.query(UsersRolesRelation).filter(UsersRolesRelation.c.id == user_role['id']).delete()
                    else:
                        roles_data.remove(user_role['role_id'])
                insert_user_roles = UsersRolesRelation.insert() \
                    .values([{'user_id': user_id, 'role_id': role} for role in roles_data])
                session.execute(insert_user_roles)
            query_result = session.query(Users).filter(Users.c.id == user_id).update(data)
            session.commit()
        return query_result

    @staticmethod
    def delete_user(user_id):
        with Session(engine) as session:
            try:
                query = session.query(Users).filter(Users.c.id == user_id)
                query_result = query.delete()
                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0
        return query_result

    @staticmethod
    def add_new_user(data):
        with Session(engine) as session:
            try:
                insert_user = Users.insert().values(full_name=data['full_name'], position=data['position'],
                                                    slack_id=data['slack_id'])
                session.execute(insert_user)
                user_id = session.query(Users.c.id).filter(Users.c.slack_id == data['slack_id']).first()['id']
                insert_user_roles = UsersRolesRelation.insert() \
                    .values([{'user_id': user_id, 'role_id': role} for role in data['roles']])
                session.execute(insert_user_roles)
                session.commit()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0
        return 1
