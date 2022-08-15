import sys
sys.path.append("..") 

from app import db
from .user import User
from .todo import Todo
from datetime import datetime
from sqlalchemy.sql import func
from dataclasses import dataclass

@dataclass
class Assignee(db.Model):
    created_at: datetime
    todo: Todo
    user: User

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, server_default=func.now(), nullable=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    todo_id = db.Column(db.Integer, db.ForeignKey('todo.id'), nullable=False)

    user = db.relationship('User', backref='user_id')
    todo = db.relationship('Todo', backref='todo')
