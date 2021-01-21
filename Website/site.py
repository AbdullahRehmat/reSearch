import random
import string
from flask_wtf import FlaskForm
from wtforms import StringField
from requests import put, post, get
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, url_for, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "Password:)"


def randomword(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class searchEngineAPI():

    def getAPI():
        api = get('http://global-api/query').json()
        return api

    def postAPI(form):
        postQuery = form.query.data
        postQuery = postQuery.lower()
        identifierString = randomword(10)

        api = post('http://global-api/query',
                   data={"identifier": identifierString, "query": postQuery}).json()

        return api


class MyForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])


@app.route('/', methods=('GET', 'POST'))
def index():
    form = MyForm()
    if form.validate_on_submit():

        searchEngineAPI.postAPI(form)
        return redirect(url_for('results'))

    return render_template('index.html', form=form)


@app.route("/results")
def results():
    searchResults = searchEngineAPI.getAPI()
    return render_template('results.html', searchResults=searchResults)


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
