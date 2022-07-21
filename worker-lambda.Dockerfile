FROM public.ecr.aws/lambda/python:3.8

COPY ./lambda_worker_source/lambda_function.py ${LAMBDA_TASK_ROOT}
COPY ./lambda_worker_source/message_services.py ${LAMBDA_TASK_ROOT}
COPY ./lambda_worker_source/orm_services.py ${LAMBDA_TASK_ROOT}
COPY ./models/models.py ${LAMBDA_TASK_ROOT}

COPY ./lambda_worker_source/requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"


CMD [ "lambda_function.lambda_handler" ]
