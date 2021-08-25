from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from models.database import Base

# Project stuff
class Project(Base):
    __tablename__ = "projects"
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    description = Column(String(250))
    # storing a list of strings in tags
    # storing a list

    tags = relationship("Tags", backref="project")
    link = Column(String(250))
    # date
    date = Column(String(50))
    # work done
    work_done = relationship("WorkDone", backref="project")

class Tags(Base):
    __tablename__ = "tags"
    id = Column(Integer, primary_key=True)
    tag = Column(String(50))
    # storing a list of strings in tags
    # storing a list

    project_id = Column(Integer, ForeignKey("projects.id"))
class WorkDone(Base):
    __tablename__ = "work_done"
    id = Column(Integer, primary_key=True)
    work = Column(String(250))
    # storing a list of strings in tags
    # storing a list

    project_id = Column(Integer, ForeignKey("projects.id"))

# User model
class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    username = Column(String(50), unique=True)
    # hashed password
    password = Column(String(250))

# Experience model
class Experience(Base):
    __tablename__ = "experience"
    id = Column(Integer, primary_key=True)
    role = Column(String(50))
    org = Column(String(50))
    date = Column(String(50))

# Languages model
class Languages(Base):
    __tablename__ = "languages"
    id = Column(Integer, primary_key=True)
    language = Column(String(50), unique=True)
    proficiency = Column(String(50))

# Domains model
class Domains(Base):
    __tablename__ = "domains"
    id = Column(Integer, primary_key=True)
    domain = Column(String(50), unique=True)

# tools model
class Tools(Base):
    __tablename__ = "tools"
    id = Column(Integer, primary_key=True)
    tool = Column(String(50), unique=True)