FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY lambda_script.py .

EXPOSE 1433

CMD ["lambda_script.handler"]