FROM amazon/aws-lambda-python:3.8

COPY ./slack_interface/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY ./slack_interface/slack_interface_message_services.py ${LAMBDA_TASK_ROOT}

COPY ./slack_interface/bonuses_function.py ${LAMBDA_TASK_ROOT}
COPY ./slack_interface/bonuses_message_services.py ${LAMBDA_TASK_ROOT}


COPY ./slack_interface/requests_function.py ${LAMBDA_TASK_ROOT}
COPY ./slack_interface/requests_message_services.py ${LAMBDA_TASK_ROOT}


COPY ./slack_interface/workers_function.py ${LAMBDA_TASK_ROOT}
COPY ./slack_interface/workers_message_services.py ${LAMBDA_TASK_ROOT}


COPY ./slack_interface/utils.py ${LAMBDA_TASK_ROOT}
COPY ./slack_interface/orm_services.py ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


CMD [ "lambda_function.lambda_handler" ]
