import os
import random
import string
from ast import literal_eval
from dotenv import load_dotenv
from flask_wtf import FlaskForm
from wtforms import StringField
from requests import put, post, get
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, url_for, jsonify, session, request, Response

app = Flask(__name__)
load_dotenv()

app.config['SECRET_KEY'] = os.getenv("FLASK_SECRET_KEY")


def generateIdentifier(length):  # Generate Random String
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class apiConn():

    def postQuery(form):  # Send Query
        query = form.query.data
        identifier = generateIdentifier(10)

        session['identifier'] = identifier
        session['query'] = query

        api = post('http://global-api/api/query',
                   data={"identifier": identifier, "query": query}).json()

        return api

    def getResults():  # Get Results
        if 'identifier' in session:
            identifier = session['identifier']
            url = str('http://global-api/api/results/') + identifier
            api = get(url).json()

            return api

        else:
            return "No Identifier was found... \n", 400


class MyForm(FlaskForm):

    query = StringField('Search', validators=[DataRequired()],
                        render_kw={"placeholder": "Search..."})


class metrix():

    def data():
        api = get('http://go-api/metrix')
        
        return api


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def index():
    form = MyForm()
    if form.validate_on_submit():

        apiConn.postQuery(form)
        return redirect(url_for('results'))

    return render_template('index.html', form=form)


@app.route("/results")
def results():
    query = session['query']
    results = list(apiConn.getResults())
    return render_template('results.html', results=results, query=query)


@app.route("/sources")
def sources():
    return render_template('sources.html')


@app.route("/admin")
def admin():
    stats = metrix.data().text
    stats = literal_eval(stats)
    stats = stats.values()
    stats = tuple(stats)

    return render_template('admin.html', stats=stats)


@app.route("/legal")
def legal():
    return render_template('legal.html')


@app.route("/robots.txt")
def robotstxt():
    r = Response(response="User-Agent: * \nAllow: /index")
    r.headers["Content-Type"] = "text/plain; charset=utf-8"
    return r


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
