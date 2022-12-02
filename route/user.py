from flask import request, Blueprint
from flask_restx import fields, Api, Resource
from flask_login import LoginManager, UserMixin, login_user
from uuid import uuid4

from context import app, swagger
from rest import request_handle, Response, BaseResource
from log import logger
from helper import sql
from model.user import User
from service import user

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
        return LoginUser(user.get_user_by_username(username))


@login_manager.user_loader
def load_user(username):
    return LoginUser.get(username)


parser = swagger.parser()
parser.add_argument('id', location='json', type=str,
                    required=True, help='Userame')
parser.add_argument('email', location='json', type=str,
                    required=False, help='Email')
parser.add_argument('password', location='json', type=str,
                    required=False, help='Password')
parser.add_argument('repassword', location='json', type=str,
                    required=False, help='rePassword')


@user_ns.route('/forget_pass')
class ForgetPassword(BaseResource):
    @user_ns.doc('change password')
    @request_handle
    def post(self):
        args = parser.parse_args()
        ret = user.update_password(
            args['id'], args['password'], args['repassword'])
        resp = Response(data={})
        resp.data = ret

        return resp


@user_ns.route('/login')
class PersonalLogin(BaseResource):
    @user_ns.doc('user login')
    @request_handle
    def post(self):
        args = parser.parse_args()
        resp = Response(data={})
        loginuser = load_user(args['id'])

        if loginuser:
            if loginuser[2] == args['password']:
                login_user(user)
            else:
                ret = 'Wrong password'
        else:
            ret = 'User not found'

        resp.data = ret
        return resp


@user_ns.route('/register')
class PersonalRegister(BaseResource):
    @user_ns.doc('user register')
    @request_handle
    def post(self):
        args = parser.parse_args()
        resp = Response(data={})
        ret = user.insert_new_user(
            args['id'], args['password'], args['repassword'], args['email'])
        resp.data = ret

        return resp


@user_ns.route('/all')
class TestList(BaseResource):
    def get(self):
        return User.query_all()
