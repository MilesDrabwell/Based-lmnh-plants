FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY extract.py .

COPY load.py .

COPY transform.py .

COPY pipeline.py .

EXPOSE 1433

ENTRYPOINT ["python3", "pipeline.py"]

#docker build -t based_plants:v1.0 . --platform "linux/amd64"

#docker tag based_plants:v1.0 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-pipeline

#docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-pipeline
