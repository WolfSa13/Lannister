FROM public.ecr.aws/lambda/python:3.8

COPY lambda_function.py ${LAMBDA_TASK_ROOT}
COPY message_services.py ${LAMBDA_TASK_ROOT}
COPY orm_services.py ${LAMBDA_TASK_ROOT}
COPY ../models/models.py ${LAMBDA_TASK_ROOT}

COPY requirements .
RUN pip install --upgrade pip && pip install -r requirements --target "${LAMBDA_TASK_ROOT}"


CMD [ "lambda_function.lambda_handler" ]