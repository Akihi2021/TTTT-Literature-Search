from flask import request, Blueprint
from flask_restx import fields, Api, Resource
from flask_login import LoginManager, UserMixin, login_user
from uuid import uuid4

from context import app, swagger
from rest import request_handle, Response, BaseResource, response_model, bool_model
from log import logger
from helper import sql
from model.user import User
from service import user

user_ns = swagger.namespace('user', description='APIs for users')
swagger.add_namespace(user_ns)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

####################################################################################################
# DEMO: Parser
# NOTE: 1. Use `remove_argument()` `replace_argument()` to either change or remove parser arguments
#       2. Use `expect` to specify expected payload
# LINK: https://flask-restx.readthedocs.io/en/latest/parsing.html#parser-inheritance

user_parser = swagger.parser()
user_parser.add_argument('id', location='json', type=str,
                         required=False, help='Userame')
user_parser.add_argument('email', location='json', type=str,
                         required=False, help='Email')
user_parser.add_argument('password', location='json', type=str,
                         required=False, help='Password')
user_parser.add_argument('repassword', location='json', type=str,
                         required=False, help='rePassword')

forget_parser = user_parser.copy()
forget_parser.remove_argument("repassword")

login_parser = forget_parser.copy()
login_parser.remove_argument("email")

####################################################################################################



class LoginUser(UserMixin):
    def __init__(self, user):
        self.username = user[1]
        self.password = user[2]
        self.email = user[4]
        self.id = user[0]

    def verify_password(self, password):
        return password == self.password

    def get_id(self):
        return self.id

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymous(self):
        return False

    @staticmethod
    def get(username):
        loginuser = user.get_user_by_username(username)
        if loginuser[0]:
            return LoginUser(loginuser[1][0])
        else:
            return None


@login_manager.user_loader
def load_user(username):
    return LoginUser.get(username)


@user_ns.route('/forget_pass')
class ForgetPassword(BaseResource):
    @user_ns.doc('change password')
    @user_ns.expect(forget_parser)
    @request_handle
    def post(self):
        args = forget_parser.parse_args()
        ret = user.update_password(
            args["id"], args["password"], args["repassword"])
        resp = Response(data={})
        resp.data = ret

        return resp


@user_ns.route('/login')
class PersonalLogin(BaseResource):
    ####################################################################################################
    # DEMO: Response Model
    # NOTE: 1. Use `namespace.model to specify the Response Model
    #       2. Use `namespace.inherit` to inherit from BaseModel(with code, msg data), to overwrite `data` part
    #       3. Use `fields.Nested for nested Data
    # LINK: https://flask-restx.readthedocs.io/en/latest/marshalling.html#nested-field
    login_result = user_ns.inherit("Login", response_model, {
        "data": fields.Nested(bool_model)
    })

    @user_ns.doc('user login')
    @user_ns.expect(login_parser)
    @user_ns.response(200, 'success', login_result)
    @request_handle
    ####################################################################################################


    def post(self):
        args = login_parser.parse_args()
        loginuser = load_user(args['id'])

        success = True
        msg = "success"

        if loginuser:
            if loginuser.password == args['password']:
                login_user(loginuser)
            else:
                logger.info("Expect:{}, Got:{}".format(loginuser.password, args['password']))
                msg = 'Wrong password'
                success = False
        else:
            msg = 'User not found'
            success = False

        resp = Response(
            msg=msg,
            data=dict(
                success=success
            ))
        return resp



@user_ns.route('/register')
class PersonalRegister(BaseResource):

    @user_ns.doc('user register')
    @user_ns.expect(user_parser)
    @request_handle
    def post(self):
        args = user_parser.parse_args()
        resp = Response(data={})
        ret = user.insert_new_user(
            args['id'], args['password'], args['repassword'], args['email'])
        resp.data = ret

        return resp


@user_ns.route('/all')
class TestList(BaseResource):
    def get(self):
        return User.query_all()
