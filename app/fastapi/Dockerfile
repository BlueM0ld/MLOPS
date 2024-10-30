FROM python:3.12

WORKDIR /fastapi

COPY . .


RUN pip install -r ./requirements.txt

CMD ["python", "main.py"]

EXPOSE 8000
