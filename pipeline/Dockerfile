FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY extract.py .

COPY load.py .

COPY transform.py .

COPY pipeline.py .

EXPOSE 1433
EXPOSE 80
EXPOSE 443

CMD ["pipeline.handler"]


#docker build -t based_plants:v1.0 . --platform "linux/amd64"

#docker tag based_plants:v1.0 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-pipeline

#docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-pipeline
