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
        self.username = user[1]
        self.password = user[2]
        self.email = user[4]
        self.id = user[0]
        self.is_associated = True if get_associated_portal(user[0])[
            0] else False

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
        if loginuser[0]:
            return LoginUser(loginuser[1][0])
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
        user = sql.select(cursor, '*', 'user',
                          "where user_name = '%s'" % username)
        success = False
        msg = "success"

        if user[0]:
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
        user = sql.select(cursor, '*', 'user',
                          "where user_name = '%s'" % username)
        db.commit()
    return user


def get_user_by_userid(userid):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user', "where id = %d" % userid)
        db.commit()
    return user


def get_associated_portal(id):
    with sql.Db_connection() as [db, cursor]:
        portal = sql.select(cursor, '*', 'portal', 'where user_id = %d' % id)
        db.commit()
    return portal


def insert_new_user(username, password, repassword, email):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user',
                          "where user_name = '%s'" % username)

        success = False
        msg = "success"

        if user[0]:
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

    if (user[0]):
        success = True
        portal = get_associated_portal(user[1][0][0])
        return msg, success, user[1][0], portal
    else:
        msg = 'The user does not exist'
        return msg, success, None, None


def update_history(history_id, user_id):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', '`user`',
                          'where id = %d' % user_id)
        success = False
        msg = "success"

        if user[0]:
            history = user[1][0][10]
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
        user = sql.select(cursor, '*', '`user`',
                          'where id = %d' % user_id)
        success = False
        msg = "success"

        if user[0]:
            follow = user[1][0][11]
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
        user = sql.select(cursor, '*', '`user`',
                          'where id = %d' % user_id)
        success = False
        msg = "success"

        if user[0]:
            favor = user[1][0][12]
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
        user = sql.select(cursor, '*', '`user`',
                          'where id = %d' % user_id)
        success = False
        msg = "success"

        if user[0]:
            user = user[1][0]
            username = info[0] if info[0] else user[1]
            gender = info[1] if info[1] else user[3]
            mail = info[2] if info[2] else user[4]
            phone = info[3] if info[3] else user[5]
            major = info[4] if info[4] else user[6]
            campus = info[5] if info[5] else user[7]
            institution = info[6] if info[6] else user[8]
            hobby = info[7] if info[7] else user[9]
            sql.update(cursor, ['user_name', 'gender', 'mail', 'phone', 'major',
                       'campus', 'institution', 'hobby'], '`user`', [username,
                       gender, mail, phone, major, campus, institution, hobby], 'where id = %d' % user_id)
            success = True
        else:
            msg = 'User not found'
        db.commit()

    return msg, success
