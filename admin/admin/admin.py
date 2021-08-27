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

@app.delete('/delete/project')
def delete_proj(project_req: DeleteProject, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(Project).filter_by(id=project_req.id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    db.delete(project)
    tags = db.query(Tags).filter_by(project_id=project_req.id).all()
    for i in tags:
        db.delete(i)
    work_done = db.query(WorkDone).filter_by(project_id=project_req.id).all()
    for i in work_done:
        db.delete(i)
    db.commit()
    db.commit()
    return {"message": "project deleted"}

 # deleting stuff
@app.delete('/delete/exp')
def delete_exp(exp_req: DeleteExperience, db: Session = Depends(get_db), user = Depends(get_current_user)):
    exp = db.query(Experience).filter_by(id=exp_req.id).first()
    if not exp:
        raise HTTPException(status_code=404, detail="Experience not found")
    db.delete(exp)
    db.commit()
    return {"message": "experience deleted"}

@app.delete('/delete/lang')
def delete_lang(lang_req: DeleteLanguage, db: Session = Depends(get_db), user = Depends(get_current_user)):
    lang = db.query(Languages).filter_by(id=lang_req.id).first()
    if not lang:
        raise HTTPException(status_code=404, detail="Language not found")
    db.delete(lang)
    db.commit()
    return {"message": "language deleted"}

@app.delete('/delete/tool')
def delete_tool(tool_req: DeleteTool, db: Session = Depends(get_db), user = Depends(get_current_user)):
    tool = db.query(Tools).filter_by(id=tool_req.id).first()
    if not tool:
        raise HTTPException(status_code=404, detail="Tool not found")
    db.delete(tool)
    db.commit()
    return {"message": "tool deleted"}

@app.delete('/delete/project/tag')
def delete_tag(tag_req: DeleteProjectTag, db: Session = Depends(get_db), user = Depends(get_current_user)):
    tag = db.query(Tags).filter_by(id=tag_req.id).first()
    if not tag:
        raise HTTPException(status_code=404, detail="Tag not found")
    db.delete(tag)
    db.commit()
    return {"message": "tag deleted"}

# UPDATES

# update project
@app.put('/update/project/tag')
def update_tag(tag_req: UpdateProjectTag, db: Session = Depends(get_db), user = Depends(get_current_user)):
    tag = db.query(Project).filter_by(project_id=tag_req.project_id)
    if not tag:
        raise HTTPException(status_code=404, detail="Project not found")
    newTag = Tags()
    newTag.tag = tag_req.tag
    newTag.project_id = tag_req.project_id
    db.add(newTag)
    db.commit()
    return {"message": "tag added"}

@app.put('/update/project/work')
def update_work(work_req: UpdateProjectWork, db: Session = Depends(get_db), user = Depends(get_current_user)):
    work = db.query(WorkDone).filter_by(project_id=work_req.project_id)
    if not work:
        raise HTTPException(status_code=404, detail="Project not found")
    newWork = WorkDone()
    newWork.work = work_req.work
    newWork.project_id = work_req.project_id
    db.add(newWork)
    db.commit()
    return {"message": "work added"}

# update project name
@app.put('/update/project/name')
def update_name(name_req: UpdateProjectName, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(Project).filter_by(project_id=name_req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.name = name_req.name
    db.commit()
    return {"message": "project name updated"}

@app.put('/update/project/desc')
def update_desc(desc_req: UpdateProjectDescription, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(Project).filter_by(project_id=desc_req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.description = desc_req.description
    db.commit()
    return {"message": "project description updated"}

@app.put('/update/project/link')
def update_link(link_req: UpdateProjectLink, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(Project).filter_by(project_id=link_req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.link = link_req.link
    db.commit()
    return {"message": "project link updated"}

@app.put('/update/project/date')
def update_date(date_req: UpdateProjectDate, db: Session = Depends(get_db), user = Depends(get_current_user)):
    project = db.query(Project).filter_by(project_id=date_req.project_id).first()
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    project.date = date_req.date
    db.commit()
    return {"message": "project date updated"}