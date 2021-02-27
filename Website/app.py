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


def randomword(length):  # Generate Random String
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class searchEngineAPI():

    def getAPI():  # Get Results
        if 'identifier' in session:
            identifier = session['identifier']
            api = get('http://global-api/api',
                      data={"identifier": identifier}).json()

            return api
        else:
            return "No Identifier was found... \n", 400

    def postAPI(form):  # Send Query
        postQuery = form.query.data
        postQuery = postQuery.title()
        identifier = randomword(10)

        session['identifier'] = identifier
        session['query'] = postQuery

        api = post('http://global-api/api',
                   data={"identifier": identifier, "query": postQuery}).json()

        return api


class MyForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()],
                        render_kw={"placeholder": "Search..."})


class matrix():

    def stats():
        api = get('http://global-api/matrix')
        return api


@app.route('/', methods=('GET', 'POST'))
@app.route('/index', methods=('GET', 'POST'))
def index():
    form = MyForm()
    if form.validate_on_submit():

        searchEngineAPI.postAPI(form)
        return redirect(url_for('results'))

    return render_template('index.html', form=form)


@app.route("/results")
def results():
    query = session['query']
    searchResults = searchEngineAPI.getAPI()
    return render_template('results.html', searchResults=searchResults, query=query)


@app.route("/sources")
def sources():
    return render_template('sources.html')


@app.route("/admin")
def admin():
    matrixStats = matrix.stats().text
    matrixStats = literal_eval(matrixStats)
    matrixMongoCS = matrixStats[0]
    matrixRedis = matrixStats[1]
    matrixMongoSE = matrixStats[2]

    return render_template('admin.html', matrixMCS=matrixMongoCS, matrixRedis=matrixRedis, matrixMSE=matrixMongoSE)

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
