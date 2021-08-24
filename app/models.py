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

    tags = relationship("Tag", backref="project")
    link = Column(String(250))
    # date
    date = Column(String(50))
    # work done
    work_done = relationship("WorkDone", backref="project")

class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(50), unique=True)
    # storing a list of strings in tags
    # storing a list

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", backref="tags")

class WorkDone(Base):
    __tablename__ = "work_done"
    id = Column(Integer, primary_key=True)
    work = Column(String(250))
    # storing a list of strings in tags
    # storing a list

    project_id = Column(Integer, ForeignKey("projects.id"))
    project = relationship("Project", backref="work_done")