from flask import request, Blueprint
from flask_restx import fields, Api, Resource
from uuid import uuid4

from context import app, swagger
from rest import request_handle, Response, BaseResource, response_model, bool_model
from log import logger
from helper import sql
from model.user import User
from service import user

user_ns = swagger.namespace('user', description='APIs for users')
swagger.add_namespace(user_ns)


####################################################################################################
# DEMO: Parser
# NOTE: 1. Use `remove_argument()` `replace_argument()` to either change or remove parser arguments
#       2. Use `expect` to specify expected payload
# LINK: https://flask-restx.readthedocs.io/en/latest/parsing.html#parser-inheritance

user_parser = swagger.parser()
user_parser.add_argument('username', location='json', type=str,
                         required=False, help='Userame')
user_parser.add_argument('email', location='json', type=str,
                         required=False, help='Email')
user_parser.add_argument('password', location='json', type=str,
                         required=False, help='Password')
user_parser.add_argument('repassword', location='json', type=str,
                         required=False, help='rePassword')

forget_parser = user_parser.copy()
forget_parser.remove_argument("email")

login_parser = forget_parser.copy()
login_parser.remove_argument("repassword")
####################################################################################################

####################################################################################################
# DEMO: Response Model
# NOTE: 1. Use `namespace.model to specify the Response Model
#       2. Use `namespace.inherit` to inherit from BaseModel(with code, msg data), to overwrite `data` part
#       3. Use `fields.Nested for nested Data
# LINK: https://flask-restx.readthedocs.io/en/latest/marshalling.html#nested-field
bool_response_model = user_ns.inherit("Login", response_model, {
    "data": fields.Nested(bool_model)
})
####################################################################################################


@user_ns.route('/forget_pass')
class ForgetPassword(BaseResource):
    @user_ns.doc('change password')
    @user_ns.expect(forget_parser)
    @user_ns.response(200, 'success', bool_response_model)
    @request_handle
    def post(self):
        args = forget_parser.parse_args()
        msg, success = user.update_password(args["username"],
                                            args["password"],
                                            args["repassword"])

        resp = Response(
            msg=msg,
            data=dict(
                success=success
            )
        )
        return resp


@user_ns.route('/login')
class PersonalLogin(BaseResource):
    @user_ns.doc('user login')
    @user_ns.expect(login_parser)
    @user_ns.response(200, 'success', bool_response_model)
    @request_handle
    def post(self):
        args = login_parser.parse_args()

        msg, success, loginuser, code = user.login(args['username'],
                                                   args['password'])

        if success:
            resp = Response(
                msg=msg,
                data=dict(
                    success=success,
                    username=loginuser.username,
                    userid=str(loginuser.id),
                    is_associated=loginuser.is_associated
                ))
        else:
            resp = Response(
                code=code,
                msg=msg,
                data=dict(
                    success=success
                ))
        return resp


@user_ns.route('/register')
class PersonalRegister(BaseResource):
    @user_ns.doc('user register')
    @user_ns.expect(user_parser)
    @user_ns.response(200, 'success', bool_response_model)
    @request_handle
    def post(self):
        args = user_parser.parse_args()

        msg, success = user.insert_new_user(args['username'],
                                            args['password'],
                                            args['repassword'],
                                            args['email'])

        resp = Response(
            msg=msg,
            data=dict(
                success=success
            )
        )
        return resp


@user_ns.route('/all')
class TestList(BaseResource):
    def get(self):
        return User.query_all()
