from fastapi import FastAPI
from fastapi.responses import FileResponse
import aiofiles
import sqlite3
import app.models as models
from sqlalchemy.orm import Session
from app.database import SessionLocal, engine

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

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
        "projects": [
                {
                    "name": "Notion-DiscordBot",
                    "description": "A link management system using Python consuming Notion API to manage links in Notion via Discord",
                    "tags": ["python", "docker", "google drive API", "notion-api"],
                    "date": "July 2021",
                    "work_done": ["Setup Google Drive API to upload files in Gdrive", "Containerised the app to run as a docker container"],
                    "link": "https://github.com/Servatom/Notion-DiscordBot"
                },
                {
                    "name": "Notefy",
                    "description": "A note-taking app with subtle yet attractive UI",
                    "tags": ["drf", "django", "HTML", "css", "React.js", "rest api"],
                    "date": "July 2021 - Present",
                    "work_done": ["Built a REST service using Django Rest framework serving React frontend", "Implemented OAuth for the application"],
                    "link": "https://github.com/Servatom/notefy"
                },
                {
                    "name": "Smart-Home-Doorbell",
                    "description": "Sends a photo to the owner of the house when a person rings the bell. Allows owner to communicate with guest",
                    "tags": ["python", "telegram-bot-api", "Raspberry Pi", "GPIO", "iOT", "IBM Watson Text-Speech API"],
                    "date": "February 2021",
                    "work_done": ["Clicking photos from an onvif camera and storing it on a server", "Used Telegram Bot library for communication", "Converts message of owner to speech for the guest", "Using a combination of raspberry pis and central hub running on linux"],
                    "link": "https://github.com/raghavTinker/Smart-Home-Doorbell"
                },
                {
                    "name": "Home-lab-server",
                    "description": "Built a homelab at home from scratch",
                    "tags": ["linux", "networking", "server management", "virtualisation", "PC building", "docker", "kubernetes"],
                    "date": "2015-Present",
                    "work_done": ["samba file server, plex media server", "replacement for time capsule to backup macOS machines over Time Machine", "virtualisation server", "custom Pfsense home router serving internet to the house. It has two WANs for failover internet access", "windows VM backups all files of linux server", "iOT lab", "docker server deployed to test out different images", "runs a VM to host https://servatom.com/"],
                    "link": ""
                },
                {
                    "name": "discord-music-bot",
                    "description": "A bot to play music from a discord channel",
                    "tags": ["python", "discord", "music", "spotify", "spotify-api", "youtube-dl player"],
                    "date": "July 2021",
                    "work_done": ["Used spotify apis and youtube-dl player to play music", "containerised the application to enable running it in a docker container"],
                    "link": "https://github.com/raghavtinker/discord-music-bot"
                }
            ]
        }
@app.get("/resume")
def resume():
    return FileResponse("app/static/resume.pdf")
