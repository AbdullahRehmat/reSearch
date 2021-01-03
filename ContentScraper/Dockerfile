FROM python:3.8-slim

WORKDIR /usr/src/app
RUN apt-get update \
&& apt-get install gcc -y \
&& apt-get clean
RUN pip install pipenv
COPY Pipfile* ./
RUN pipenv lock --requirements > requirements.txt
RUN pip install -r requirements.txt

COPY . .
CMD [ "python", "./redistest.py" ]
