from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
import aiofiles
import sqlite3
import app.models as models
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine
from pydantic import BaseModel
from typing import List
from app.models import Project, Tags, WorkDone
from fastapi.security import HTTPBasic, HTTPBasicCredentials
import secrets
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

class ProjectCreate(BaseModel):
    name: str
    description: str
    date: str
    tags: List[str]
    work_done: List[str]
    link: str

def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()

# security
# get username and password from environment OS

username = os.getenv("USERNAME")
password = os.getenv("PASSWORD")

print(username)
print(password)

security = HTTPBasic()

def get_current_username(credentials: HTTPBasicCredentials = Depends(security)):
    correct_username = secrets.compare_digest(credentials.username, username)
    correct_password = secrets.compare_digest(credentials.password, password)
    if not (correct_username and correct_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )
    return credentials.username

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
def projects():
    return {
        "projects": []
        }

@app.post("/createproject")
def createproject(project_req: ProjectCreate, db: Session = Depends(get_db), username: str = Depends(get_current_username)):
    project = Project()
    project.name = project_req.name
    project.description = project_req.description
    project.date = project_req.date
    project.link = project_req.link
    try:
        db.add(project)
        db.commit()
    except:
        return {"error": "project already added"}
    # get project id
    project_id = db.query(Project.id).filter(Project.name == project_req.name).first()
    project_id = project_id[0]

    print(project_id)
    for i in project_req.tags:
        tags = Tags()
        tags.tag = i
        tags.project_id = project_id
        db.add(tags)
    
    for i in project_req.work_done:
        work_done = WorkDone()
        work_done.work = i
        work_done.project_id = project_id
        db.add(work_done)
    
    db.commit()
    return {"message": "Project created"}

@app.get("/resume")
def resume():
    return FileResponse("app/static/resume.pdf")
