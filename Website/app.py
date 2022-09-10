import os
import random
import string
from ast import literal_eval
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField
from requests import post, get
from wtforms.validators import DataRequired
from flask import Flask, Response, render_template, redirect, url_for, session

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['API_HOST'] = os.getenv("API_HOSTNAME")


def generate_identifier(length):
    """ Generates Random String For Use As An Identifier """

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class ApiConn():

    def post_query(query):
        """ Sends query recieved to API for processing via POST """

        identifier = generate_identifier(10)

        # Add Identifier and Query to Session
        session['identifier'] = identifier
        session['query'] = query

        # Assemble URL and Payload
        url = str(f"http://{app.config['API_HOST']}/api/v1/query")
        payload = {"identifier": identifier, "query": query}

        # Send POST Request
        api = post(url, json=payload)

        return api

    def get_response():
        """ Collects response from API via unique ID """

        if 'identifier' in session:
            identifier = session['identifier']

            url = str(
                f"http://{app.config['API_HOST']}/api/v1/results/{identifier}")

            data = get(url).json()
            time_taken = data["time_taken"]
            results = data["results"]

            return str(time_taken), results

        else:
            return "No Identifier was found... \n", 400


class MyForm(FlaskForm):

    query = StringField("Search", validators=[DataRequired()],
                        render_kw={"placeholder": "Search..."})


class Metrix():

    def data():
        """ Sends Search Engine Useage Data to Client """

        api = get(f"http://{app.config['API_HOST']}/api/v1/metrix")

        return api


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def index():
    form = MyForm()
    if form.validate_on_submit():

        ApiConn.post_query(form.query.data)
        return redirect(url_for('results'))

    return render_template('index.html', form=form)


@app.route("/results")
def results():
    query = session['query']
    time_taken, results = ApiConn.get_response()

    return render_template('results.html', time_taken=time_taken, results=results, query=query)


@app.route("/sources")
def sources():
    return render_template('sources.html')


@app.route("/admin")
def admin():
    data = Metrix.data().text
    data = literal_eval(data)
    data = data["data"]
    data = tuple(data.values())

    return render_template('admin.html', stats=data, api=app.config['API_HOST'])


@app.route("/legal")
def legal():
    return render_template('legal.html')


@app.route("/robots.txt")
def robots_txt():
    r = Response(response="User-Agent: * \nAllow: /index")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
