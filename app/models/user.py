import sys
sys.path.append("..") 

import enum
from app import db
from typing import Type, Dict
from flask_login import UserMixin
from dataclasses import dataclass

class Role(str, enum.Enum):
    Developer = 'Developer'
    ProjectManager = 'ProjectManager'

@dataclass
class User(db.Model, UserMixin):
    id: int
    name: str
    role: "Role"
    email: str
    username: str

    id = db.Column(db.Integer, primary_key=True)
    is_active = db.Column(db.Boolean, default=1, nullable=False)
    name = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    role = db.Column(db.Enum(Role), default=Role.Developer, nullable=False)