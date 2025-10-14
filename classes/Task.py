from sqlalchemy.orm import declarative_base
from sqlalchemy import Column, Integer, String, Boolean

Base = declarative_base()

class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True)

    _title = Column("title", String)
    _description = Column("description", String)
    _complete = Column("complete", Boolean, default=False)

    def __init__(self, title, description):
        self.setTitle(title)
        self.setDescription(description)

    def getInfo(self):
        return {
            "id": self.id,
            "title": self._title,
            "description": self._description,
            "complete": self._complete
        }

    def setComplete(self, is_complete: bool):
        self._complete = is_complete

    def setTitle(self, title: str):
        self._title = title

    def setDescription(self, description: str):
        self._description = description
