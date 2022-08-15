import json
from app import bcrypt
from models import User
from datetime import timedelta
from routes import app, login_manager, db
from flask import Response, request, session
from flask_bcrypt import Bcrypt, generate_password_hash, check_password_hash
from flask_login import UserMixin, login_user, LoginManager, current_user, logout_user, login_required
from sqlalchemy.exc import IntegrityError,DataError, DatabaseError, InterfaceError, InvalidRequestError

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.before_request
def session_handler():
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=90)

@app.route("/login", methods=["POST"], strict_slashes=False)
def login():
    response = Response(response=json.dumps({ "success": True, "message": "Succesfully signed-in!" }), status=200)
    response.headers["content-type"] = "application/json"
    try:
        user = User.query.filter_by(email=request.form['email']).first()
        if check_password_hash(user.password, request.form['password']):
            login_user(user)
        else:
            response = Response(response=json.dumps({ "success": False, "message": "Invalid username or password!" }), status=403)
    except Exception as e:
        print(e)
        response = Response(response=json.dumps({ "success": False, "message": "Something went wrong!" }), status=500)
    return response

@app.route("/register", methods=["POST"], strict_slashes=False)
def register():
    response = Response(response=json.dumps({ "success": True, "message": "Account succesfully created!" }), status=201)
    response.headers["content-type"] = "application/json"
    try:        
        newuser = User(
            name=request.form['name'],
            role=request.form['role'],
            email=request.form['email'],
            username=request.form['username'],
            password=bcrypt.generate_password_hash(request.form['password'])
        )

        db.session.add(newuser)
        db.session.commit()
    except IntegrityError:
        db.session.rollback()
        response = Response(response=json.dumps({ "success": False, "message": "User already exists!" }), status=422)
    except DataError:
        db.session.rollback()
        response = Response(response=json.dumps({ "success": False, "message": "Invalid Entry!" }), status=422)
    except (InterfaceError, DatabaseError):
        db.session.rollback()
        response = Response(response=json.dumps({ "success": False, "message": "Error connecting to the database!" }), status=500)
    except Exception as e:
        print(e)
        db.session.rollback()
        response = Response(response=json.dumps({ "success": False, "message": "Something went wrong!" }), status=500)
    return response

@app.route("/logout")
@login_required
def logout():
    logout_user()
    response = Response(response=json.dumps({ "success": True, "message": "Succesfully signed-out!" }), status=200)
    response.headers["content-type"] = "application/json"
    return response