from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    __title = Column("title", String)
    __description = Column("description", String)
    __complete = Column("complete", Boolean, default=False)
    __priority= Column("priority", Integer, default=3)

    def __init__(self, title, description, priority):
        self.setTitle(title)
        self.setDescription(description)
        self.setPriority(priority)

    def getInfo(self):
        return {
            "id": self.id,
            "title": self.__title,
            "description": self.__description,
            "complete": self.__complete,
            "priority": self.__priority
        }

    def setComplete(self, is_complete):
        if not isinstance(is_complete, bool):
            raise TypeError("Nieprawidłowy typ danych - oczekiwano: bool")
        self.__complete = is_complete

    def setPriority(self, priority):
        if not isinstance(priority, int):
            raise TypeError("Nieprawidłowy typ danych - oczekiwano: int")
        if priority>3 or priority<1:
            raise ValueError("Wartość poza oczekiwanym zakresem")
        self.__priority = priority

    def setTitle(self, title):
        if not isinstance(title, str):
            raise TypeError("Nieprawidłowy typ danych - oczekiwano: string")
        if title == "":
            raise ValueError("Pole nie może być puste")
        if len(title)>100:
            raise ValueError("Tekst zbyt długi")
        self.__title = title

    def setDescription(self, description):
        if not isinstance(description, str):
            raise TypeError("Nieprawidłowy typ danych - oczekiwano: string")
        if description == "":
            raise ValueError("Pole nie może być puste")
        if len(description)>300:
            raise ValueError("Tekst zbyt długi")
        self.__description = description
