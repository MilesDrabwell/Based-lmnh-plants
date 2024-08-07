FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

EXPOSE 1433

#129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-pipeline

#docker build -t based_plants:v0.0 . --platform "linux/amd64"

#docker tag based_plants:v0.0 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-pipeline

#docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-pipeline