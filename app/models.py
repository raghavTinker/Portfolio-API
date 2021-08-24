from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import Base

class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(250))
    # storing a list of strings in tags
    # storing a list

    tags = Column(list())
    link = Column(String(250))
    # date
    date = Column(String(50))
    # work done
    work_done = Column(list())
    