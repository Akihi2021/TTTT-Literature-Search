from flask import request, Blueprint
from flask_restx import fields, Api, Resource
from flask_login import LoginManager, UserMixin
from uuid import uuid4

from main import app, swagger
from rest import request_handle, Response, BaseResource
from log import logger
from models import User

##################################################
# Demo route with URL query
##################################################
user_ns = swagger.namespace('user', description='APIs for users')
swagger.add_namespace(user_ns)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class LoginUser(UserMixin):


@user_ns.route('/forget_pass')
class ForgetPassword(BaseResource):
    @user_ns.doc('change password')
    @user_ns.param('Email', 'Email', type=str)
    @user_ns.param('id', 'username', type=str)
    @user_ns.param('password', 'password', type=str)
    @user_ns.param('rePassword', 'rePassword', type=str)
    @request_handle
    def post(self):
        email = str(request.args['Email'])
        username = str(request.args['id'])
        password = str(request.args['password'])
        repassword = str(request.args['rePassword'])
        user = User()
        resp = Response()

        if user.query_by_username_and_email(username, email):
            if repassword == password:
                user.update_password(username, email, password)
            else:
                resp.msg = 'The two passwords are inconsistent'
        else:
            resp.msg = 'User not found'
        return resp


@user_ns.router('/login')
class PersonalLogin(BaseResource):
    @user_ns.doc('user login')
    @user_ns.param('id', 'username', type=str)
    @user_ns.param('password', 'password', type=str)
    @request_handle
    def post(self):
        username = str(request.args['id'])
        password = str(request.args['password'])
        user = User()
        resp = Response()
