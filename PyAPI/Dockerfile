FROM python:3.8-slim

WORKDIR /usr/src/app
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "-w", "2", "-b", ":80", "--reload", "wsgi:app"]