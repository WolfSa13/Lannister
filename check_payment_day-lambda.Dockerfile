FROM amazon/aws-lambda-python:3.8

COPY ./lambda_check_payment_day/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY ./lambda_check_payment_day/message_services.py ${LAMBDA_TASK_ROOT}
COPY ./lambda_check_payment_day/orm_services.py ${LAMBDA_TASK_ROOT}
COPY ./lambda_check_payment_day/time_utils.py ${LAMBDA_TASK_ROOT}
COPY ./models/models.py ${LAMBDA_TASK_ROOT}

COPY ./lambda_check_payment_day/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


CMD [ "lambda_function.lambda_handler" ]
