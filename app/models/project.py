import sys
sys.path.append("..") 

from app import db
from .user import User
from datetime import datetime
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Project(db.Model):
    id: int
    created_at: datetime
    owner: User
    title: str
    description: str
    deleted_at: datetime

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text, nullable=False)
    deleted_at = db.Column(db.DateTime, default=None, nullable=True)
    owner = db.relationship('User', backref='user')
