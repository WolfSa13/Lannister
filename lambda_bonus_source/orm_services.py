import sqlalchemy as db
from sqlalchemy.orm.session import Session
import os

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')


class TypeBonusesQuery:
    engine = db.create_engine(
        f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
    metadata = db.MetaData(engine)
    db.MetaData.reflect(metadata)

    TypeBonuses = metadata.tables['type_bonus']

    @staticmethod
    def get_bonuses(bonus_id=None):
        with Session(TypeBonusesQuery.engine) as session:
            query = session.query(TypeBonusesQuery.TypeBonuses).order_by(TypeBonusesQuery.TypeBonuses.columns.id)

            if bonus_id is not None:
                query = query.filter(TypeBonusesQuery.TypeBonuses.columns.id == bonus_id)

            query_result = query.all()
            result = []
            for bonus in query_result:
                result.append(
                    {
                        "id": bonus[0],
                        "type": bonus[1],
                        "description": bonus[2]
                    }
                )

        return result

    @staticmethod
    def update_bonuses(bonus_id, data):
        with Session(TypeBonusesQuery.engine) as session:
            query = session.query(TypeBonusesQuery.TypeBonuses)
            query = query.filter(TypeBonusesQuery.TypeBonuses.columns.id == bonus_id)
            query.update(data)

            session.commit()

            # query_result = TypeBonusesQuery.get_bonuses()

        return 1

    @staticmethod
    def delete_bonuses(bonus_id):
        with Session(TypeBonusesQuery.engine) as session:
            try:
                query = session.query(TypeBonusesQuery.TypeBonuses).filter(TypeBonusesQuery.TypeBonuses.columns.id == bonus_id)
                query.delete()

                session.commit()
                query_result = TypeBonusesQuery.get_bonuses()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return query_result

    @staticmethod
    def add_new_bonus(data):
        with Session(TypeBonusesQuery.engine) as session:
            try:
                insert = TypeBonusesQuery.TypeBonuses.insert().values(type=data['type'], description=data['description'])
                session.execute(insert)
                session.commit()

                result = TypeBonusesQuery.get_bonuses()
            except db.exc.SQLAlchemyError as e:
                session.rollback()
                return 0

        return 1
