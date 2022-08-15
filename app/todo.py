import json
from routes import app, db
from models import Todo, Role
from flask_restful import Resource
from flask import Response, request, jsonify
from flask_login import login_required, current_user

class TodosResource(Resource):
    @login_required
    def get(self):
        return jsonify(Todo.query.filter_by(deleted_at=None).all())

class TodoResource(Resource):
    @login_required
    def get(self, todo_id):
        return jsonify(Todo.query.filter_by(id=todo_id, deleted_at=None).all())

    @login_required
    def post(self):
        todo = Todo(
            created_by=current_user.id,
            project_id=request.form['project_id'],
            title=request.form['title'],
            body=request.form['body'],
            deleted_at=None 
        )
        db.session.add(todo)
        db.session.commit()

        return Response(status=204)

    @login_required
    def put(self, todo_id):
        todo = self.fetch_todo(todo_id)

        if not todo:
            return Response(status=404)
        
        todo.body = request.form['body']
        todo.title = request.form['title']
        todo.project_id = request.form['project_id']
        db.session.add(todo)
        db.session.commit()

        return Response(status=204)

    @login_required
    def delete(self, todo_id):
        todo = self.fetch_todo(todo_id)

        if not todo:
            return Response(status=404)

        db.session.delete(todo)
        db.session.commit()

        return Response(status=204)

    def fetch_todo(self, todo_id):
        if current_user.role == Role.ProjectManager:
            return Todo.query.filter_by(id=todo_id, deleted_at=None).first()
        else:
            return Todo.query.filter_by(id=todo_id, created_by=current_user.id, deleted_at=None).first()

class UserTodoResource(Resource):
    @login_required
    def get(self, user_id):
        return jsonify(Todo.query.filter_by(created_by=user_id, deleted_at=None).all())
        