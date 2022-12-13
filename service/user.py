from config import *
from helper import sql
from context import db, app
from flask_login import LoginManager, UserMixin, login_user
from log import logger


login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


class LoginUser(UserMixin):
    def __init__(self, user):
        self.username = user['user_name']
        self.password = user['password']
        self.email = user['mail']
        self.id = user['id']
        self.is_associated = user['openalex_id'] if user['openalex_id'] else False

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
        loginuser = get_user_by_username(username)
        if loginuser:
            return LoginUser(loginuser)
        else:
            return None


@login_manager.user_loader
def load_user(username):
    return LoginUser.get(username)


def login(id, password):
    success = True
    msg = "success"
    user = load_user(id)
    code = 200

    if user:
        if user.password == password:
            login_user(user)
        else:
            logger.info("Expect:{}, Got:{}".format(user.password, password))
            msg = 'Wrong password'
            success = False
            code = 0
    else:
        msg = 'User not found'
        success = False
        code = 800

    return msg, success, user, code


def update_password(username, password, repassword):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', 'user',
                               "where user_name = '%s'" % username)
        success = False
        msg = "success"

        if num:
            if repassword == password:
                sql.update(cursor, ['password'], '`user`', [
                    password], "where user_name = '%s'" % username)
                success = True
            else:
                msg = 'The two passwords are inconsistent'
        else:
            msg = 'User not found'
        db.commit()

    return msg, success


def get_user_by_username(username):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', 'user',
                               "where user_name = '%s'" % username)
        db.commit()
    return user[0] if num else None


def get_user_by_userid(userid):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', 'user', "where id = %d" % userid)
        db.commit()
    return user[0] if num else None


def insert_new_user(username, password, repassword, email):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', 'user',
                               "where user_name = '%s'" % username)

        success = False
        msg = "success"

        if num:
            msg = 'User already exists'
        else:
            if repassword == password:
                sql.insert(cursor, 'user', [
                           'user_name', 'password', 'mail'], [username, password, email])
                success = True
            else:
                msg = 'The two passwords are inconsistent'

        db.commit()

    return msg, success


def get_user_info(user_id):
    success = False
    msg = "success"
    user = get_user_by_userid(user_id)

    if (user):
        success = True
        return msg, success, user
    else:
        msg = 'The user does not exist'
        return msg, success, None, None


def update_history(history_id, user_id):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', '`user`',
                               'where id = %d' % user_id)
        success = False
        msg = "success"

        if num:
            user = user[0]
            history = user['history']
            if history:
                history_list = eval(history)
                history_list.insert(0, history_id)
                history = str(history_list)
            else:
                history_list = []
                history_list.insert(0, history_id)
                history = str(history_list)
            sql.update(cursor, ['history'], '`user`', [
                history], 'where id = %d' % user_id)
            success = True
        else:
            msg = 'User not found'
        db.commit()

        return msg, success


def update_following(following_id, user_id):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', '`user`',
                               'where id = %d' % user_id)
        success = False
        msg = "success"

        if num:
            user = user[0]
            follow = user['follow']
            if follow:
                follow_list = eval(follow)
                follow_list.insert(0, following_id)
                follow = str(follow_list)
            else:
                follow_list = []
                follow_list.insert(0, following_id)
                follow = str(follow_list)
            sql.update(cursor, ['follow'], '`user`', [
                follow], 'where id = %d' % user_id)
            success = True
        else:
            msg = 'User not found'
        db.commit()

        return msg, success


def update_favor(favor_id, user_id):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', '`user`',
                               'where id = %d' % user_id)
        success = False
        msg = "success"

        if num:
            user = user[0]
            favor = user['favor']
            if favor:
                favor_list = eval(favor)
                favor_list.insert(0, favor_id)
                favor = str(favor_list)
            else:
                favor_list = []
                favor_list.insert(0, favor_id)
                favor = str(favor_list)
            sql.update(cursor, ['favor'], '`user`', [
                favor], 'where id = %d' % user_id)
            success = True
        else:
            msg = 'User not found'
        db.commit()

        return msg, success


def update_info(user_id, info):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', '`user`',
                               'where id = %d' % user_id)
        success = False
        msg = "success"

        if num:
            user = user[0]
            username = info['user_name'] if info['user_name'] else user['user_name']
            gender = info['gender'] if info['gender'] else user['gender']
            mail = info['mail'] if info['mail'] else user['mail']
            phone = info['phone'] if info['phone'] else user['phone']
            major = info['major'] if info['major'] else user['major']
            department = info['department'] if info['department'] else user['department']
            institution = info['institution'] if info['institution'] else user['institution']
            hobby = info['hobby'] if info['hobby'] else user['hobby']
            language = info['language'] if info['language'] else user['language']
            introduction = info['introduction'] if info['introduction'] else user['introduction']
            position = info['position'] if info['position'] else user['position']
            org_bio = info['org_bio'] if info['org_bio'] else user['org_bio']
            achievement = info['achievement'] if info['achievement'] else user['achievement']
            direction = info['direction'] if info['direction'] else user['direction']
            sql.update(cursor, ['user_name', 'gender', 'mail', 'phone', 'major',
                       'department', 'institution', 'hobby', 'language', 'introduction', 'position', 'org_bio', 'achievement', 'direction'], '`user`', [username,
                       gender, mail, phone, major, department, institution, hobby, language, introduction, position, org_bio, achievement, direction], 'where id = %d' % user_id)
            success = True
        else:
            msg = 'User not found'
        db.commit()

    return msg, success


def associate_user(user_id, expert_id):
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', '`user`',
                               'where id = %d' % user_id)
        success = False
        msg = "success"

        if num:
            sql.update(cursor, ['openalex_id'], '`user`', [
                       expert_id], 'where id = %d' % user_id)
            success = True
        else:
            msg = 'User not found'
        db.commit()

    return msg, success
