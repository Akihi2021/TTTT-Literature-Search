from config import *
from helper import sql


def updata_password(username, password, repassword):
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


# def create_user(user_name, password, mail):
#     with sql.Db_connection() as [db, cursor]:
#         sql.insert(cursor, 'user', ['user_name', 'password', 'mail'], [
#             user_name, password, mail])
#         db.commit()
#
#
# def query_by_username_and_email(user_name, email):
#     with sql.Db_connection() as [db, cursor]:
#         obj = sql.select(cursor, ['*'], 'user',
#                          'where user_name = %s and mail = %s' % (user_name, email))
#     if obj:
#         obj = cls(user_name=obj['user_name'],
#                   password=obj['password'], mail=obj['mail'])
#     return obj.decode()
#
#
# def query_by_username(user_name):
#     with sql.Db_connection() as [db, cursor]:
#         obj = sql.select(cursor, ['*'], 'user',
#                          'where user_name = %s' % user_name)
#     if obj:
#         obj = cls(user_name=obj['user_name'],
#                   password=obj['password'], mail=obj['mail'])
#     return obj.decode()
#
#
# def update_password(password):
#     with sql.Db_connection() as [db, cursor]:
#         obj = sql.update(cursor, ['password'], 'user', [password],
#                          'where user_name = %s' % self.user_name)
#         db.commit()
#     return self