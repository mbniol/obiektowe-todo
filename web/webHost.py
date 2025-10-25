import flask
import modules.objectLib as ol

app = flask.Flask(__name__)
db=ol.dbSelfHost()

@app.route("/")
def index():
    return flask.render_template('index.html', getall=ol.getAll(db))


@app.errorhandler(404)
def not_found(e):
  return flask.render_template("404.html")