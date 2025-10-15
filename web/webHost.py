import flask
import modules.objectLib as ol

app = flask.Flask(__name__)
db=ol.dbSelfHost()

@app.route("/")
def hello_world():
    return flask.render_template('index.html', getall=ol.getAll(db))