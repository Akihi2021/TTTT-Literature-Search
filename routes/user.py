from flask import request, Blueprint
from flask_restx import fields, Api, Resource
from flask_login import LoginManager, UserMixin, login_user
from uuid import uuid4

from main import app, swagger
from rest import request_handle, Response, BaseResource
from log import logger
from models import User
from helper import sql

##################################################
# Demo route with URL query
##################################################
user_ns = swagger.namespace('user', description='APIs for users')
swagger.add_namespace(user_ns)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class LoginUser(UserMixin):
    def __init__(self, user):
        self.username = user.decode().user_name
        self.password = user.decode().password
        self.email = user.decode().email
        self.id = user.id

    def verify_password(self, password):
        return password == self.password

    def get_id(self):
        return self.id

    @staticmethod
    def get(username):
        with sql.Db_connection("127.70.14.86", "root",
                               "Buaa2022", "tttt") as [db, cursor]:
            user = sql.select(cursor, '*', 'user',
                              'where user_name = %s' % username)
            db.commit()
        if not user:
            return None
        return LoginUser(user)


@login_manager.user_loader
def load_user(username):
    return LoginUser.get(username)


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
        resp = Response()

        with sql.Db_connection("127.70.14.86", "root",
                               "Buaa2022", "tttt") as [db, cursor]:
            user = sql.select(cursor, '*', 'user',
                              'where user_name = %s' % username)
            if user:
                if repassword == password:
                    sql.update(cursor, ['password'], 'user', [password])
                else:
                    resp.msg = 'The two passwords are inconsistent'
            else:
                resp.msg = 'User not found'
        return resp


@user_ns.route('/login')
class PersonalLogin(BaseResource):
    @user_ns.doc('user login')
    @user_ns.param('id', 'username', type=str)
    @user_ns.param('password', 'password', type=str)
    @request_handle
    def post(self):
        username = str(request.args['id'])
        password = str(request.args['password'])
        resp = Response()
        user = load_user(username)

        if user:
            if user.verify_password(password):
                login_user(user)
            else:
                resp.msg = 'Wrong password'
        else:
            resp.msg = 'User not found'

        return resp


@user_ns.route('/register')
class PersonalRegister(BaseResource):
    @user_ns.doc('user register')
    @user_ns.param('id', 'username', type=str)
    @user_ns.param('password', 'password', type=str)
    @user_ns.param('repassword', 'rePassword', type=str)
    @user_ns.param('Email', 'Email', type=str)
    @request_handle
    def post(self):
        email = str(request.args['Email'])
        username = str(request.args['id'])
        password = str(request.args['password'])
        repassword = str(request.args['repassword'])
        resp = Response()

        user = User.query_by_username(username)
        if user:
            resp.msg = 'User already exists'
        else:
            if password == repassword:
                with sql.Db_connection("127.70.14.86", "root",
                                       "Buaa2022", "tttt") as [db, cursor]:
                    user = sql.insert(cursor, 'user', ['user_name', 'password', 'mail'], [
                                      username, password, email])
                    db.commit()
            else:
                resp.msg = 'The two passwords are inconsistent'

        return resp
