FROM python:3.12

WORKDIR /streamlit

COPY . .

RUN pip install -r ./requirements.txt

EXPOSE 8501

CMD ["streamlit", "run", "streamlit_app.py", "–server.port=8501","--server.address=0.0.0.0"]

