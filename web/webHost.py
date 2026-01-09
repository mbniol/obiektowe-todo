import flask
import modules.objectLib as ol

app = flask.Flask(__name__)
db=ol.dbSelfHost()
ol.clearTasks(db)
ol.mock(10,db)

@app.route("/")
def index():
    return flask.render_template('index.html', getall=ol.getAll(db))

@app.route("/task")
def taskView():
    task_id = flask.request.args.get('id', type=int)
    return flask.render_template('task.html', taskinfo=ol.getTask(task_id,db))


@app.errorhandler(404)
def not_found(e):
  return flask.render_template("404.html")