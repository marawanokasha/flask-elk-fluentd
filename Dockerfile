FROM python:3.6

COPY ./requirements.txt /tmp/requirements.txt

RUN pip install --upgrade pip
RUN pip install -r /tmp/requirements.txt
RUN pip install uwsgi

COPY . /app
WORKDIR /app

EXPOSE 8080

CMD ["uwsgi",  "--ini", "uwsgi.ini"]
