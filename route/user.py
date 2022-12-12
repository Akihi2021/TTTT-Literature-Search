from flask import request, Blueprint
from flask_restx import fields, Api, Resource
from uuid import uuid4

from context import app, swagger
from rest import request_handle, Response, BaseResource, response_model
from log import logger
from helper import sql
from model.user import User
from service import user

user_ns = swagger.namespace('user', description='APIs for User')
swagger.add_namespace(user_ns)


####################################################################################################
# DEMO: Parser
# NOTE: 1. Use `remove_argument()` `replace_argument()` to either change or remove parser arguments
#       2. Use `expect` to specify expected payload
# LINK: https://flask-restx.readthedocs.io/en/latest/parsing.html#parser-inheritance

login_parser = swagger.parser()
login_parser.add_argument('username', type=str,
                          required=True, location="json", help='Userame')
login_parser.add_argument('password', type=str,
                          required=True, location="json", help='Password')

forget_parser = login_parser.copy()
forget_parser.add_argument('repassword', type=str,
                           required=True, location="json",  help='rePassword')

register_parser = forget_parser.copy()
register_parser.add_argument(
    'email', type=str, required=True, location="json",  help='Email')

id_parser = swagger.parser()
id_parser.add_argument('user_id', type=int, required=True,
                       location="json",   help='UserId')

history_parser = id_parser.copy()
history_parser.add_argument(
    'paper_id', type=str, required=True, location="json",  help='latest viewed paper')

favor_parser = id_parser.copy()
favor_parser.add_argument('paper_id', type=str,
                          required=True, location="json",  help='latest favored paper')

follow_parser = id_parser.copy()
follow_parser.add_argument('expert_id', type=str,
                           required=True, location="json",  help='latest followed expert')

update_parser = id_parser.copy()
update_parser.add_argument('user_name', location="json",  type=str,
                           required=False, default=None, help='username')
update_parser.add_argument(
    'gender', type=str, required=False, location="json",  default=None, help='gender')
update_parser.add_argument(
    'mail', type=str, required=False, location="json",  default=None, help='email')
update_parser.add_argument(
    'phone', type=str, required=False, location="json",  default=None, help='phone')
update_parser.add_argument(
    'major', type=str, required=False, location="json",  default=None, help='major')
update_parser.add_argument(
    'campus', type=str, required=False, location="json",  default=None, help='campus')
update_parser.add_argument('institution', type=str,
                           required=False, location="json",  default=None, help='institution')
update_parser.add_argument(
    'hobby', type=str, required=False, location="json",  default=None, help='hobby')
update_parser.add_argument(
    'language', type=str, required=False, location="json",  default=None, help='language')
update_parser.add_argument('introduction', location="json",  type=str,
                           required=False, default=None, help='introduction')
update_parser.add_argument('position', location="json",
                           type=str, required=False, default=None, help='position')
update_parser.add_argument('org_bio', location="json",
                           type=str, required=False, default=None, help='org bio')
update_parser.add_argument('achievement', location="json",
                           type=str, required=False, default=None, help='achievement')

associate_parser = id_parser.copy()
associate_parser.add_argument(
    'expert_id', type=str, location="json",  required=True, help='ExpertId')
####################################################################################################

####################################################################################################
# DEMO: Response Model
# NOTE: 1. Use `namespace.model to specify the Response Model
#       2. Use `namespace.inherit` to inherit from BaseModel(with code, msg data), to overwrite `data` part
#       3. Use `fields.Nested for nested Data
# LINK: https://flask-restx.readthedocs.io/en/latest/marshalling.html#nested-field
success_data_model = swagger.model("SuccessData", model={
    "success": fields.Boolean(False)
})

success_response_model = user_ns.inherit("SuccessResponse", response_model, {
    "data": fields.Nested(success_data_model)
})

login_success_data_model = user_ns.inherit("LoginSuccessData", success_data_model, {
    "username": fields.String,
    "userid": fields.Integer,
    "is_associated": fields.Boolean
})

login_success_response_model = user_ns.inherit("LoginSuccessResponse", response_model, {
    "data": fields.Nested(login_success_data_model)
})

user_info_data_model = user_ns.inherit("UserInfoData", success_data_model, {
    "username": fields.String,
    "gender": fields.String,
    "email": fields.String,
    "phone": fields.String,
    "major": fields.String,
    "campus": fields.String,
    "org": fields.String,
    "is_associated": fields.Boolean,
    "department": fields.String,
    "history": fields.List(fields.String),
    "follow": fields.List(fields.String),
    "favor": fields.List(fields.String),
    "language": fields.String,
    "introduction": fields.String,
    'position': fields.String,
    'org_bio': fields.String,
    'achievement': fields.String
})

user_info_response_model = user_ns.inherit("UserInfoResponse", response_model, {
    "data": fields.Nested(user_info_data_model)
})
####################################################################################################


@user_ns.route('/forget_pass')
class ForgetPassword(BaseResource):
    @user_ns.doc('change password')
    @user_ns.expect(forget_parser)
    @user_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = forget_parser.parse_args()
        msg, success = user.update_password(args["username"],
                                            args["password"],
                                            args["repassword"])

        code = 200 if success else 0

        resp = Response(
            code=code,
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
    @user_ns.response(200, 'success', login_success_response_model)
    @user_ns.response(800, 'fail', success_response_model)
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
    @user_ns.expect(register_parser)
    @user_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = register_parser.parse_args()

        msg, success = user.insert_new_user(args['username'],
                                            args['password'],
                                            args['repassword'],
                                            args['email'])

        code = 200 if success else 0

        resp = Response(
            code=code,
            msg=msg,
            data=dict(
                success=success
            )
        )
        return resp


@user_ns.route('/check_my_info')
class CheckInfo(BaseResource):
    @user_ns.doc('check user info')
    @user_ns.expect(id_parser)
    @user_ns.response(200, 'success', user_info_response_model)
    @request_handle
    def post(self):
        args = id_parser.parse_args()

        msg, success, infouser = user.get_user_info(
            args['user_id'])

        code = 200 if success else 0

        resp = Response(
            code=code,
            msg=msg,
            data=dict(
                success=success,
                username=infouser['user_name'] if success else None,
                gender=infouser['gender'] if success else None,
                email=infouser['mail'] if success else None,
                phone=infouser['phone'] if success else None,
                major=infouser['major'] if success else None,
                campus=infouser['campus'] if success else None,
                org=infouser['institution'] if success else None,
                is_associated=(True if infouser['openalex_id']
                               else False) if success else None,
                department=infouser['institution'] if success else None,
                hobby=infouser['hobby'] if success else None,
                history=(eval(infouser['history'])if infouser['history']
                         else []) if success else None,
                follow=(eval(infouser['follow'])if infouser['follow']
                        else []) if success else None,
                favor=(eval(infouser['favor']) if infouser['favor']
                       else []) if success else None,
                language=infouser['language'] if success else None,
                introduction=infouser['introduction'] if success else None,
                position=infouser['position'] if success else None,
                org_bio=infouser['org_bio'] if success else None,
                achievement=infouser['achievement'] if success else None
            )
        )
        return resp


@user_ns.route('/update_viewed_history')
class UpdateViewedHistory(BaseResource):
    @user_ns.doc('update user\'s viewed history')
    @user_ns.expect(history_parser)
    @user_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = history_parser.parse_args()

        msg, success = user.update_history(args['paper_id'], args['user_id'])

        code = 200 if success else 0

        resp = Response(
            code=code,
            msg=msg,
            data=dict(
                success=success
            )
        )
        return resp


@user_ns.route('/update_following')
class UpdateViewedHistory(BaseResource):
    @user_ns.doc('update user\'s following list')
    @user_ns.expect(follow_parser)
    @user_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = follow_parser.parse_args()

        msg, success = user.update_following(
            args['expert_id'], args['user_id'])

        code = 200 if success else 0

        resp = Response(
            code=code,
            msg=msg,
            data=dict(
                success=success
            )
        )
        return resp


@user_ns.route('/update_favor_list')
class UpdateViewedHistory(BaseResource):
    @user_ns.doc('update user\'s favor list')
    @user_ns.expect(favor_parser)
    @user_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = favor_parser.parse_args()

        msg, success = user.update_favor(args['paper_id'], args['user_id'])

        code = 200 if success else 0

        resp = Response(
            code=code,
            msg=msg,
            data=dict(
                success=success
            )
        )
        return resp


@user_ns.route('/update_user_info')
class UpdateUserInfo(BaseResource):
    @user_ns.doc('update user\'s info')
    @user_ns.expect(update_parser)
    @user_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = update_parser.parse_args()

        info = dict(
            user_name=args['user_name'],
            gender=args['gender'],
            mail=args['mail'],
            phone=args['phone'],
            major=args['major'],
            campus=args['campus'],
            institution=args['institution'],
            hobby=args['hobby'],
            language=args['language'],
            introduction=args['introduction'],
            position=args['position'],
            org_bio=args['org_bio'],
            achievement=args['achievement']
        )

        msg, success = user.update_info(args['user_id'], info)

        code = 200 if success else 0

        resp = Response(
            code=code,
            msg=msg,
            data=dict(
                success=success
            )
        )
        return resp


@user_ns.route('/associate_user')
class AssociateUser(BaseResource):
    @user_ns.doc('associate user with expert')
    @user_ns.expect(associate_parser)
    @user_ns.response(200, 'success', success_response_model)
    @request_handle
    def post(self):
        args = associate_parser.parse_args()

        msg, success = user.associate_user(args['user_id'], args['expert_id'])

        code = 200 if success else 0

        resp = Response(
            code=code,
            msg=msg,
            data=dict(
                success=success
            )
        )

        return resp


@ user_ns.route('/all')
class TestList(BaseResource):
    def get(self):
        return User.query_all()
