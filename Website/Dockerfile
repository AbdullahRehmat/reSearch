FROM python:3.8-slim

WORKDIR /usr/src/app

RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD ["gunicorn", "-w", "2", "-b", ":8000", "--reload", "wsgi:app"]