import json
from routes import app, db
from models import Project, Role
from flask_restful import Resource
from flask import Response, request, jsonify
from flask_login import login_required, current_user

class ProjectsResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        if not current_user or not current_user.is_authenticated or current_user.role != Role.ProjectManager:
            return Response(response="", status=403)
        return super(ProjectsResource, self).dispatch_request(*args, **kwargs)

    @login_required
    def get(self):
        return jsonify(Project.query.filter_by(deleted_at=None).all())

class ProjectResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        if not current_user or not current_user.is_authenticated or current_user.role != Role.ProjectManager:
            return Response(response="", status=403)
        return super(ProjectResource, self).dispatch_request(*args, **kwargs)

    @login_required
    def get(self, project_id):
        return jsonify(Project.query.filter_by(id=project_id, deleted_at=None).all())

    @login_required
    def post(self):
        project = Project(
            created_by=current_user.id,
            title=request.form['title'],
            description=request.form['description'],
            deleted_at=None 
        )
        db.session.add(project)
        db.session.commit()

        return Response(status=204)

    @login_required
    def put(self, project_id):
        project = self.fetch_project(project_id)

        if not project:
            return Response(status=404)
        
        project.body = request.form['body']
        project.description = request.form['description']
        db.session.add(project)
        db.session.commit()

        return Response(status=204)

    @login_required
    def delete(self, project_id):
        project = self.fetch_project(project_id)

        if not project:
            return Response(status=404)

        db.session.delete(project)
        db.session.commit()

        return Response(status=204)

    def fetch_project(self, project_id):
        if current_user.role == Role.ProjectManager:
            return Project.query.filter_by(id=project_id, deleted_at=None).first()
        else:
            return Project.query.filter_by(id=project_id, created_by=current_user.id, deleted_at=None).first()
        