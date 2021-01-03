from requests import put, post, get
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, url_for, jsonify

app = Flask(__name__)
app.config['SECRET_KEY'] = "Password:)"


class searchEngineAPI():

    def getAPI():
        api = get('http://global-api/query').json()
        return api

    def postAPI(form):
        postQuery = form.query.data
        postQuery = postQuery.lower()
        postIdentifier = "Query"
        api = post('http://global-api/query',
                   data={"identifier": postIdentifier, "query": postQuery}).json()
        return api


class MyForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()])


@app.route('/', methods=('GET', 'POST', 'PUT'))
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
