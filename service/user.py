from config import *
from helper import sql


def update_password(username, password, repassword):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user',
                          'where user_name = %s' % username)
        if user:
            if repassword == password:
                sql.update(cursor, ['password'], 'user', [password])
            else:
                ret = 'The two passwords are inconsistent'
        else:
            ret = 'User not found'

        return ret


def get_user_by_username(username):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user',
                          'where user_name = %s' % username)
    return user


def insert_new_user(username, password, repassword, email):
    with sql.Db_connection() as [db, cursor]:
        user = sql.select(cursor, '*', 'user',
                          'where user_name = %s' % username)
        if user:
            ret = 'User already exists'
        else:
            if repassword == password:
                sql.insert(cursor, 'user', [
                           'user_name', 'password', 'mail'], [username, password, email])
            else:
                ret = 'The two passwords are inconsistent'

        return ret
