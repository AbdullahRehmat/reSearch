import random
import string
from flask_wtf import FlaskForm
from wtforms import StringField
from requests import put, post, get
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, url_for, jsonify, session

app = Flask(__name__)
app.config['SECRET_KEY'] = "Password:)"


def randomword(length):  # Generate Random String
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


class searchEngineAPI():

    def getAPI():  # Get Results from Global API
        if 'identifier' in session:
            identifier = session['identifier']
            api = get('http://global-api/api',
                      data={"identifier": identifier}).json()

            return api
        else:
            return "No Identifier was found... \n", 400

    def postAPI(form):  # Send Query to GlobalAPI
        postQuery = form.query.data
        postQuery = postQuery.title()
        identifier = randomword(10)

        session['identifier'] = identifier
        session['query'] = postQuery

        api = post('http://global-api/api',
                   data={"identifier": identifier, "query": postQuery}).json()

        return api


class MyForm(FlaskForm):
    query = StringField('Search', validators=[DataRequired()], render_kw={
                        "placeholder": "Search..."})

class matrix():

    def getMatrix():
        api = get('http://global-api/matrix')

        return api



@app.route('/', methods=('GET', 'POST'))
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
 

@app.route("/admin")
def admin():
    queryCount = matrix.getMatrix()
    queryCount=queryCount.text

    return render_template('admin.html', queryCount=queryCount)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == "__main__":
    app.run(host='0.0.0.0', port='80', debug=True)
