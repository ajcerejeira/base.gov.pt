FROM python:3.6

WORKDIR /app

COPY requirements.txt /requirements.txt
RUN pip install -r /requirements.txt
COPY . /app

CMD ["python", "go-spider.py"]