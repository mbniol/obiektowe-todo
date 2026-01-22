import flask
import modules.objectLib as ol
from classes.EditType import EditType
import secrets
from flask_wtf import FlaskForm, CSRFProtect
from wtforms import StringField, SubmitField, RadioField, TextAreaField
from wtforms.validators import DataRequired, Length, InputRequired

app = flask.Flask(__name__)
db=ol.dbSelfHost()

foo = secrets.token_urlsafe(16)
app.secret_key = foo

csrf = CSRFProtect(app)

class AddForm(FlaskForm):
    title = StringField('Tytuł:')
    description = TextAreaField('Opis:')
    priority = RadioField('Priorytet:',validators=[InputRequired(message=None)],choices=[(1,"Wysoki"),(2,"Średni"),(3,"Niski")])
    submit = SubmitField('Dodaj')

class EditForm(FlaskForm):
    title = StringField('Tytuł:')
    description = TextAreaField('Opis:')
    priority = RadioField('Priorytet:', validators=[InputRequired()],choices=[(1,"Wysoki"),(2,"Średni"),(3,"Niski")],coerce=int)
    submit = SubmitField('Zapisz zmiany')

@app.route("/")
def index():
    return flask.render_template('index.html', getall=ol.getAll(db))

@app.route('/add',methods=['GET', 'POST'])
def addTask():
    form = AddForm()
    message = ""
    if form.validate_on_submit():
        response = ol.createTask(form.title.data,form.description.data,int(form.priority.data),db)
        if isinstance(response, int):
            return flask.redirect("/")
        else:
            message = response
    return flask.render_template('add.html', form=form, message=message)

@app.route("/task")
def taskView():
    task_id = flask.request.args.get('id', type=int)
    return flask.render_template('task.html', taskinfo=ol.getTask(task_id,db))

@app.route("/edit", methods=['GET', 'POST'])
def editTask():
    task_id = flask.request.args.get('id', type=int)
    where_from = flask.request.args.get('from', type=str)
    task_data = ol.getTask(task_id, db)
    
    if task_data==-1:
        return flask.abort(404)

    form = EditForm()
    message = ""

    if form.validate_on_submit():
        results = [
            ol.editTask(task_id, EditType.TITLE, form.title.data, db),
            ol.editTask(task_id, EditType.DESC, form.description.data, db),
            ol.editTask(task_id, EditType.PRIOR, int(form.priority.data), db),
        ]

        error = next((r for r in results if not isinstance(r, int)), None)

        if error is None:
            if where_from == 'task':
                return flask.redirect(f"/task?id={task_id}")
            return flask.redirect("/")
        else:
            message = error

    if not form.is_submitted():
        form.title.data = task_data['title']
        form.description.data = task_data['description']
        form.priority.data = int(task_data['priority'])

    return flask.render_template('edit.html', form=form, taskinfo=task_data, where_from=where_from, message=message)

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
    where_from = flask.request.args.get('from', type=str)
    ol.editTask(task_id, EditType.COMPL, False, db)

    if where_from == 'task':
        return flask.redirect("/task?id="+str(task_id))
    else:
        return flask.redirect("/")


@app.route("/setcomp1")
def setcomp1():
    task_id = flask.request.args.get('id', type=int)
    where_from = flask.request.args.get('from', type=str)
    ol.editTask(task_id, EditType.COMPL, True, db)

    if where_from == 'task':
        return flask.redirect("/task?id="+str(task_id))
    else:
        return flask.redirect("/")

@app.errorhandler(404)
def not_found(e):
  return flask.render_template("404.html")