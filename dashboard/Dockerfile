FROM python:latest

COPY requirements.txt .

RUN pip3 install -r requirements.txt

COPY .streamlit .streamlit/

COPY dashboard.py .
COPY get_long_term.py .
EXPOSE 8501

CMD streamlit run dashboard.py --server.port=8501