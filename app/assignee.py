import json
from routes import app, db
from models import Assignee, Role
from flask_restful import Resource
from flask import Response, request, jsonify
from flask_login import login_required, current_user

class AssigneeResource(Resource):
    def dispatch_request(self, *args, **kwargs):
        if not current_user or not current_user.is_authenticated or current_user.role != Role.ProjectManager:
            return Response(response="", status=403)
        return super(AssigneeResource, self).dispatch_request(*args, **kwargs)

    @login_required
    def post(self):
        assignee = Assignee(
            user_id=request.form['user_id'],
            todo_id=request.form['todo_id'],
        )
        db.session.add(assignee)
        db.session.commit()

        return Response(status=204)