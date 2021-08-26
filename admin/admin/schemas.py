from pydantic import BaseModel
from typing import List

class ProjectCreate(BaseModel):
    name: str
    description: str
    date: str
    tags: List[str]
    work_done: List[str]
    link: str

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
    