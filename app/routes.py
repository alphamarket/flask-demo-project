from flask_restful import Api
from app import create_app, db, login_manager

app = create_app()

from auth import *
from todo import *
from project import *
from assignee import *

api = Api(app)
api.add_resource(TodosResource, '/todos')
api.add_resource(TodoResource, '/todo/<int:todo_id>', '/todo')
api.add_resource(ProjectsResource, '/projects')
api.add_resource(ProjectResource, '/project/<int:project_id>', '/project')
api.add_resource(AssigneeResource, '/asign')
api.add_resource(UserTodoResource, '/user/<int:user_id>/todos')

if __name__ == "__main__":
    app.run(debug=True)