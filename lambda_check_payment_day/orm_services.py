import sqlalchemy as db
from sqlalchemy.orm.session import Session
from sqlalchemy.sql.expression import ColumnElement as ColElem
from datetime import date
import os

from models import Request, User, Bonus

POSTGRES_USER = os.environ.get('POSTGRES_USER')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')
POSTGRES_HOST = os.environ.get('POSTGRES_HOST')
POSTGRES_PORT = os.environ.get('POSTGRES_PORT')
POSTGRES_DB = os.environ.get('POSTGRES_DB')

engine = db.create_engine(
    f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}')
metadata = db.MetaData(engine)
db.MetaData.reflect(metadata)


class RequestQuery:
    # import requests
    #
    # BASE_URL = 'https://cdka1dmmkj.execute-api.us-east-1.amazonaws.com/test'
    # url = f'{BASE_URL}/requests?type=6'
    #
    # response = requests.get(url=url)
    @staticmethod
    def get_requests_by_payment_date():
        current_date = date.today().strftime("%Y-%m-%d")

        with Session(engine) as session:
            creator = db.orm.aliased(User)
            reviewer = db.orm.aliased(User)
            query = session.query(Request.id, Request.payment_amount, Request.created_at,
                                  Request.description, Bonus.type,
                                  ColElem.label(creator.full_name, 'creator_name'),
                                  ColElem.label(reviewer.slack_id, 'reviewer_slack_id'))
            query = query.filter(Request.status == 'approved').filter(Request.payment_date == str(current_date))

            query = query.join(creator, Request.creator == creator.id) \
                .join(reviewer, Request.reviewer == reviewer.id) \
                .join(Bonus, Request.type_bonus == Bonus.id)

            query_result = query.all()

        return RequestQuery._parsed_requests(query_result)

    @staticmethod
    def _parsed_requests(requests):
        parsed_result = dict()
        requests = [dict(request) for request in requests]

        for request in requests:
            slack_id = request.pop('reviewer_slack_id')
            if slack_id not in parsed_result:
                parsed_result[slack_id] = [request]
            else:
                parsed_result[slack_id].append(request)

        return parsed_result
