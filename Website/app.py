"""
    Python Webserver Powered By Flask.
"""

import os
import random
import string
from ast import literal_eval
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField
from requests import post, get
from wtforms.validators import DataRequired
from flask import Flask, Response, render_template, redirect, url_for

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")
app.config['API_HOST'] = os.getenv("API_HOSTNAME")


def generate_identifier(length):
    """ Generates Random String For Use As An Identifier """

    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class API():

    def post_query(identifier, query):
        """ Sends Unique ID & Query To API For Processing """

        # Assemble URL and Payload
        url = str(f"http://{app.config['API_HOST']}/api/v1/search")
        payload = {"identifier": identifier, "query": query}

        # Send POST Request
        api = post(url, json=payload)

        return api

    def get_results(identifier):
        """ Returns Response From API Via Unique ID """

        if identifier != "":

            url = str(
                f"http://{app.config['API_HOST']}/api/v1/results/{identifier}")

            data = get(url).json()

            return data["query"], data["results"], data["time_taken"]

        else:
            return "No Identifier Provided... \n", 400

    def get_metrix():
        """ Returns Search Engine Usage Data """

        api = get(f"http://{app.config['API_HOST']}/api/v1/metrix")

        return api


class SearchForm(FlaskForm):

    query = StringField("Search", validators=[DataRequired()],
                        render_kw={"placeholder": "Search..."})


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def index():

    identifier = generate_identifier(10)

    form = SearchForm()

    if form.validate_on_submit():

        API.post_query(identifier, form.query.data)

        return redirect(url_for('results', identifier=identifier))

    return render_template('index.html', form=form)


@app.route("/results/<identifier>")
def results(identifier):

    query, results, time_taken = API.get_results(identifier)

    return render_template('results.html', query=query, results=results,
                           time_taken=time_taken)


@app.route("/sources")
def sources():
    return render_template('sources.html')


@app.route("/admin")
def admin():
    data = API.get_metrix().text
    data = literal_eval(data)
    data = data["data"]
    data = tuple(data.values())

    return render_template('admin.html', stats=data,
                           api=app.config['API_HOST'])


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
