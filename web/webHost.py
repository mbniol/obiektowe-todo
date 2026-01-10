import flask
import modules.objectLib as ol
from classes.EditType import EditType

app = flask.Flask(__name__)
db=ol.dbSelfHost()
ol.clearTasks(db)

@app.route("/")
def index():
    return flask.render_template('index.html', getall=ol.getAll(db))

@app.route("/task")
def taskView():
    task_id = flask.request.args.get('id', type=int)
    return flask.render_template('task.html', taskinfo=ol.getTask(task_id,db))

@app.route("/clear")
def clear():
    ol.clearTasks(db)
    return flask.redirect("/")

@app.route("/mock")
def mock():
    ol.mock(10,db)
    return flask.redirect("/")

@app.route("/del")
def delete():
    task_id = flask.request.args.get('id', type=int)
    ol.deleteTask(task_id,db)
    return flask.redirect("/")

@app.route("/setcomp0")
def setcomp0():
    task_id = flask.request.args.get('id', type=int)
    ol.editTask(task_id, EditType.COMPL, False, db)
    return flask.redirect("/")

@app.route("/setcomp1")
def setcomp1():
    task_id = flask.request.args.get('id', type=int)
    ol.editTask(task_id, EditType.COMPL, True, db)
    return flask.redirect("/")

@app.errorhandler(404)
def not_found(e):
  return flask.render_template("404.html")