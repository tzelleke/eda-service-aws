FROM public.ecr.aws/lambda/python:3.10
COPY requirements.txt ${LAMBDA_TASK_ROOT}
RUN pip install -r requirements.txt --no-cache-dir
COPY perform_eda.py ${LAMBDA_TASK_ROOT}
CMD [ "perform_eda.handler" ]
