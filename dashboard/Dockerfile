FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY .streamlit .streamlit/

COPY dashboard.py .
COPY get_long_term.py .
EXPOSE 8501

CMD streamlit run dashboard.py --server.port=8501

# aws ecr get-login-password --region eu-west-2 | docker login --username AWS --password-stdin 129033205317.dkr.ecr.eu-west-2.amazonaws.com
# docker build -t based_dashboard:v1.0 . --platform "linux/amd64"
# docker tag based_dashboard:v1.0 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-dashboard
# docker push 129033205317.dkr.ecr.eu-west-2.amazonaws.com/c12-based-dashboard