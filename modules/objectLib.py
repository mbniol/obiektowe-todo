from classes.Task import Task, Base
from classes.EditType import EditType
from classes.Priority import Priority
import random

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
    try:
        new_task = Task(title,description,priority)
        session.add(new_task)
        session.commit()
    except Exception as e:
        return e
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
        return 0
    else:
        return 1

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
                try:
                    task.setTitle(change_to)
                except Exception as e:
                    return e
                return 0
            case EditType.DESC:
                try:
                    task.setDescription(change_to)
                except Exception as e:
                    return e
                return 0
            case EditType.PRIOR:
                try:
                    task.setPriority(change_to)
                except Exception as e:
                    return e
                return 0
            case EditType.COMPL:
                try:
                    task.setComplete(change_to)
                except Exception as e:
                    return e
                return 0
    
def getAll(session):
    """Zwraca listę wszystkich zadań w formie listy słowników.
    
    Parametry:
    -sesja DB
    """
    tasks = session.query(Task).all()
    return [task.getInfo() for task in tasks]

def mock(number, session):
    titles = ["pomocy uwiezili mnie w tasku", "losowy tytul", "lorem ipsum", "radia posłuchać", "pojeść","smacznej kawusi"]
    descriptions = ["test", "i wtedy ten sloik pekł", "dzien dobry", "3 dnia zastali pusty grub", "Pyszny i łatwy do przygotowania bigos z kiszonej kapusty z mięsem wieprzowym, kiełbasą, suszonymi grzybami. Zobacz także: bigos z kapusty białej i kiszonej"]
    for i in range(number):
        tit = random.choice(titles)
        desc = random.choice(descriptions)
        prio = random.randint(1,3)
        createTask(tit, desc, prio, session)