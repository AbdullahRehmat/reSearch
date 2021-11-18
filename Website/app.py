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


def generate_identifier(length):  # Generate Random String
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class ApiConn():

    def post_query(query):
        """ Sends query recieved to API for processing via POST """

        identifier = generate_identifier(10)
        session['identifier'] = identifier
        session['query'] = query

        api = post('http://global-api/api/query',
                   data={"identifier": identifier, "query": query}).json()

        return api

    def get_results():
        """ Collects response from API via unique ID """

        if 'identifier' in session:
            identifier = session['identifier']
            url = str('http://global-api/api/results/') + identifier
            api = get(url).json()

            # This needs refactoring
            # If Else Stack ensures that the api returns a list
            # Needs to be fixed by the API!
            if type(api) == str:
                print("Recived String. Converted to JSON")
                return literal_eval(api)
            elif type(api) != str:
                print("Recived JSON.")
                return api
            else:
                return ['An Error Occured!']

        else:
            return "No Identifier was found... \n", 400


class MyForm(FlaskForm):

    query = StringField('Search', validators=[DataRequired()],
                        render_kw={"placeholder": "Search..."})


class Metrix():

    def data():
        api = get('http://go-api/metrix')

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
    results = list(ApiConn.get_results())
    return render_template('results.html', results=results, query=query)


@app.route("/sources")
def sources():
    return render_template('sources.html')


@app.route("/admin")
def admin():
    stats = Metrix.data().text
    stats = literal_eval(stats)
    stats = stats.values()
    stats = tuple(stats)

    return render_template('admin.html', stats=stats)


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
