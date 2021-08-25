from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import FileResponse
import aiofiles
import sqlite3
import api.models as models
from sqlalchemy.orm import Session
from api.database import SessionLocal, engine
from api.schemas import *
from api.models import Project, Tags, WorkDone, UserModel, Tools, Domains, Languages, Experience
from api.security import *
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

# security

@app.post('/signup')
def signup(user_req: UserCreate, db: Session = Depends(get_db)):
    # has passwd
    try:
        user = UserModel(username=user_req.username, password=hashMe(user_req.password))
        db.add(user)
        db.commit()
        return {"status": "user_created"}
    except:
        return {"status": "user_exists"}


@app.post('/login')
def login(user_req: UserLogin, db: Session = Depends(get_db)):
    user = db.query(UserModel).filter_by(username=user_req.username).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if not verify_passwd(user_req.password, user.password):
        raise HTTPException(status_code=401, detail="Incorrect creds")
    

    access_token = create_access_token(user.username)
    return {"access_token": access_token, "type": "bearer"}


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
    return FileResponse("app/static/resume.pdf")


# Admin stuff

@app.post("/createproject")
def createproject(project_req: ProjectCreate, db: Session = Depends(get_db), user = Depends(get_current_user)):
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

@app.post('/create_exp')
def createExp(experience_req: ExperienceCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        experience = Experience()
        experience.role = experience_req.role
        experience.org = experience_req.org
        experience.date = experience_req.date
    except:
        return {"error": "error in creating experience"}
        
@app.post('/languages')
def createLanguages(languages_req: LanguageCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        languages = Languages()
        languages.language = languages_req.language
        languages.proficiency = languages_req.proficiency
        db.add(languages)
        db.commit()
    except:
        return {"error": "error in creating languages"}

@app.post('/tools')
def createTools(tools_req: ToolCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        tools = Tools()
        tools.tool = tools_req.tool
        db.add(tools)
        db.commit()
    except:
        return {"error": "error in creating tools"}

@app.post('/createdomains')
def createDomains(domains_req: DomainCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        domains = Domains()
        domains.domain = domains_req.domain

        # add to db
        db.add(domains)
        db.commit()

        return {"message": "domain created {}".format(domains_req.domain)} 
    except:
        return {"error": "error in creating domains"}