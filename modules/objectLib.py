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
    tasks = session.query(Task).order_by("complete", "priority", "title").all()
    return [task.getInfo() for task in tasks]

def mock(number, session):
    titles = ["pomocy uwiezili mnie w tasku", "losowy tytul", "lorem ipsum", "radia posłuchać", "pojeść","smacznej kawusi","we are charlie kirk"]
    descriptions = ["test", "i wtedy ten sloik pekł", "dzien dobry", "3 dnia zastali pusty grub", "Pyszna tarta z gruszką i serem gorgonzola to idealne połączenie słodyczy z wyrazistym smakiem. Przygotowanie zacznij od wyłożenia formy do pieczenia gotowym ciastem francuskim, które należy nakłuć widelcem i podpiec przez kilka minut w piekarniku nagrzanym do dwustu stopni. W tym czasie przygotuj nadzienie, krojąc dojrzałe gruszki w cienkie plasterki oraz krusząc w dłoniach ser z niebieską pleśnią. Na podpieczony spód wyłóż warstwę serka mascarpone wymieszanego z odrobiną miodu i świeżym rozmarynem. Następnie ułóż promieniście plastry owoców, a wolne przestrzenie wypełnij kawałkami gorgonzoli oraz garścią posiekanych orzechów włoskich, które dodadzą całości przyjemnej chrupkości. Całość wstaw ponownie do pieca na około piętnaście minut, aż brzegi ciasta staną się złociste, a ser apetycznie się rozpuści. Po wyjęciu z piekarnika tartę warto skropić gęstym octem balsamicznym lub dodatkową strużką miodu dla przełamania smaków."]
    for i in range(number):
        tit = random.choice(titles)
        desc = random.choice(descriptions)
        prio = random.randint(1,3)
        createTask(tit, desc, prio, session)