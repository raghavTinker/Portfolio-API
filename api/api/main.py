from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
import aiofiles
import sqlite3
import models.models as models
from sqlalchemy.orm import Session
from models.database import SessionLocal, engine
from models.models import Project, Tags, WorkDone, UserModel, Tools, Domains, Languages, Experience
import os

from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Routes

@app.get("/")
def profile():
    return {"name": "Raghav Sharma", 
            "contact": {
                "phone": "+91 9880918485", 
                "email": "raghav.sharma17@outlook.com", 
                "linkedin": "https://in.linkedin.com/in/raghavtinker",
                "github": "https://github.com/raghavTinker"
            },
            "about": "A tech enthusiast, and an avid programmer. Currently, I am in my second year at Thapar Institute of Technology pursuing my bachelor's in Computer Science engineering. I create innovative solutions for everyday problems. I am a hardworking student who enjoys tinkering with electronics and aims to solve core issues with technology. My domain is mainly in backend development, DevOps, and automation.",
            "paths": {
                "homepage": "https://raghavtinker.servatom.com/",
                "experience": "https://raghavtinker.servatom.com/exp",
                "skills": "https://raghavtinker.servatom.com/skills",
                "projects": "https://raghavtinker.servatom.com/projects",
                "resume": "https://raghavtinker.servatom.com/resume"
            }
        }

@app.get("/exp")
def experience():
    return {
            "experience":{
                "Microsoft Learn Student Chapter" : ["Executive Member", "2021-present"],
                "Linux User Group": ["Executive Member", "2020-present"]
            }
        }

@app.get("/skills")
def skills():
    return {
            "languages": ["Python", "C", "C++", "Swift", "Bash Scripting"],
            "tools": ["git", "github", "travis-ci", "vs-code", "vim", "linux", "Jupyter Notebooks", "docker", "k8s"],
            "domains": ["DevOps", "Automation", "iOT", "server management", "iOS app development"]
        }

@app.get("/projects")
def projects(db: Session = Depends(get_db)):
    # get all the projects from the database

    projectsList = []

    for project in db.query(Project).all():
        json = {}
        print(project.name)
        json["name"] = project.name
        json["description"] = project.description
        json["date"] = project.date
        json["link"] = project.link

        tags = []
        work_done = []
        for tagObj in project.tags:
            tags.append(tagObj.tag)
        json["tags"] = tags
        for workObj in project.work_done:
            work_done.append(workObj.work)
        json["work_done"] = work_done
        projectsList.append(json)
    
    return {
        "projects": projectsList
        }

@app.get("/resume")
def resume():
    return FileResponse("database/static/resume.pdf")