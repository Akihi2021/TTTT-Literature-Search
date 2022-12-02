from config import *
from helper import sql
from context import db


def update_password(username, password, repassword):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user',
                          "where user_name = '%s'" % username)
        if user[0]:
            if repassword == password:
                sql.update(cursor, ['password'], '`user`', [
                    password], "where user_name = '%s'" % username, True)
                ret = None
            else:
                ret = 'The two passwords are inconsistent'
        else:
            ret = 'User not found'
        db.commit()

    return ret


def get_user_by_username(username):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user',
                          "where user_name = '%s'" % username)
        db.commit()
    return user


def insert_new_user(username, password, repassword, email):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user',
                          "where user_name = '%s'" % username)
        if user[0]:
            ret = 'User already exists'
        else:
            if repassword == password:
                sql.insert(cursor, 'user', [
                           'user_name', 'password', 'mail'], [username, password, email])
                ret = None
            else:
                ret = 'The two passwords are inconsistent'

        db.commit()

    return ret
