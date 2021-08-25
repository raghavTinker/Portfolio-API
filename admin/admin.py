from fastapi import FastAPI, Depends, HTTPException, status
from admin.schemas import *
from models.models import Project, Tags, WorkDone, UserModel, Tools, Domains, Languages, Experience
from admin.security import *
import models.models as models
from models.database import SessionLocal, engine
from admin.schemas import *
from models.models import Project, Tags, WorkDone, UserModel, Tools, Domains, Languages, Experience
from sqlalchemy.orm import Session

app = FastAPI()
models.Base.metadata.create_all(bind=engine)


def get_db():
    try :
        db = SessionLocal()
        yield db
    finally:
        db.close()

# Admin stuff
@app.get("/")
def index():
    return {"message": "Hello World"}


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
        db.add(experience)
        db.commit()
        return {"message": "Experience created"}
    except:
        return {"error": "error in creating experience"}
        
@app.post('/create_lang')
def createLanguages(languages_req: LanguageCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        languages = Languages()
        languages.language = languages_req.language
        languages.proficiency = languages_req.proficiency
        db.add(languages)
        db.commit()
        return {"message": "Language added"}
    except:
        return {"error": "error in creating languages"}

@app.post('/create_tool')
def createTools(tools_req: ToolCreate, user = Depends(get_current_user), db: Session = Depends(get_db)):
    try:
        tools = Tools()
        tools.tool = tools_req.tool
        db.add(tools)
        db.commit()
        return {"message": "Tool added"}
    except:
        return {"error": "error in creating tools"}

@app.post('/create_domain')
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