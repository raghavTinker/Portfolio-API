from pydantic import BaseModel
from typing import List

class ProjectCreate(BaseModel):
    name: str
    description: str
    date: str
    tags: List[str]
    work_done: List[str]
    link: str
    repo_link: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class LanguageCreate(BaseModel):
    language: str
    proficiency: str

class ToolCreate(BaseModel):
    tool: str

class DomainCreate(BaseModel):
    domain: str

class ExperienceCreate(BaseModel):
    role: str
    org: str
    date: str

class DeleteProject(BaseModel):
    id: int

class DeleteProjectTag(BaseModel):
    id: int

class DeleteExperience(BaseModel):
    id: int

class UpdateProjectTag(BaseModel):
    project_id: int
    tag: str

class UpdateProjectWork(BaseModel):
    project_id: int
    work_done: str

class UpdateProjectName(BaseModel):
    project_id: int
    name: str

class UpdateProjectDescription(BaseModel):
    project_id: int
    description: str

class UpdateProjectLink(BaseModel):
    project_id: int
    link: str

class UpdateProjectRepoLink(BaseModel):
    project_id: int
    repo_link: str

class UpdateProjectDate(BaseModel):
    project_id: int
    date: str

class DeleteLanguage(BaseModel):
    id: int

class DeleteTool(BaseModel):
    id: int