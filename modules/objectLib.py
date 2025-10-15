from classes.Task import Task, Base
from classes.EditType import EditType

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

"""
Zawiera zestaw funkcji do obsługi tasków

do dokonczenia :c
"""


def dbSelfHost():
    """Tworzy instancje bazy danych i zwraca obiekt sesji"""
    engine = create_engine("sqlite:///tasks.db")
    Base.metadata.create_all(engine)
    Session = sessionmaker(bind=engine)
    session = Session()
    return session

def createTask(title, description, priority, session):
    """Tworzy nowego taska i zwraca jego ID
    
    Parametry:
    -tytul
    -opis
    -sesja DB
    """
    new_task = Task(title,description,priority)
    session.add(new_task)
    session.commit()
    return new_task.id

def deleteTask(id,session):
    """Usuwa taska z danym ID
    
    Parametry:
    -ID
    -sesja DB
    """
    task = session.get(Task, id)
    if task:
        session.delete(task)
        session.commit()

def clearTasks(session):
    """Usuwa wyszstkie taski
    
    Parametry:
    -sesja DB
    """
    session.query(Task).delete()
    session.commit()

def getTask(id,session):
    """Pobiera i zwraca dane dla taska z podanym ID, jezeli ten task nie istnieje zwraca -1
    
    Parametry:
    -ID
    -sesja DB
    """
    task = session.get(Task, id)
    if task:
        return task.getInfo()
    else:
        return -1
    
def editTask(id,field,change_to,session):
    task = session.get(Task, id)
    if task:
        match field:
            case EditType.TITLE:
                task.setTitle(change_to)
            case EditType.DESC:
                task.setDescription(change_to)
            case EditType.PRIOR:
                task.setPriority(change_to)
            case EditType.COMPL:
                task.setComplete(change_to)
    
def getAll(session):
    """Zwraca listę wszystkich zadań w formie listy słowników.
    
    Parametry:
    -sesja DB
    """
    tasks = session.query(Task).all()
    return [task.getInfo() for task in tasks]