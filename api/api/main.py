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
def experience(db: Session = Depends(get_db)):
    jobs = []
    for exp in db.query(Experience).all():
        job = {
            "id": exp.id,
            "organisation": exp.org,
            "role": exp.role,
            "duration": exp.date,
        }
        jobs.append(job)
    return {
            "experience": jobs
        }

@app.get("/skills")
def skills(db: Session = Depends(get_db)):
    # get languages in an array
    languages = []
    for lang in db.query(Languages).all():
        languages.append({"language": lang.language, "proficiency": lang.proficiency})
    
    tools = []
    for tool in db.query(Tools).all():
        tools.append(tool.tool)

    print(tools)
    
    domains = []
    for domain in db.query(Domains).all():
        domains.append(domain.domain)
    return {
            "languages": languages,
            "tools": tools,
            "domains": domains
        }

@app.get("/projects")
def projects(db: Session = Depends(get_db)):
    # get all the projects from the database

    projectsList = []

    for project in db.query(Project).all():
        json = {}
        print(project.name)
        json["id"] = project.id
        json["name"] = project.name
        json["description"] = project.description
        json["date"] = project.date
        json["link"] = project.link
        json["repo_link"] = project.repo_link

        tags = []
        work_done = []
        for tagObj in project.tags:
            tags.append(tagObj.tag)
        json["tags"] = tags
        for workObj in project.work_done:
            work_done.append(workObj.work)
        json["work_done"] = work_done
        projectsList.append(json)
    db.close()
    return {
        "projects": projectsList
        }

@app.get("/resume")
def resume():
    return FileResponse("database/static/resume.pdf")