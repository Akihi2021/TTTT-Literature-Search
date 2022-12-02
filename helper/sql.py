import pymysql
from config import *

##################################################
## sql database utils
##################################################


class Db_connection:
    # Demo:
    # A Connection to db can be initialized as following

    # with Db_connection(config['db_host'], config['db_user'], \
    #                    config['db_passwd'], config['db_database'], config['db_port']) \
    #         as [db, cursor]:
    #     now_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    #     for k,v in video_label.items():
    #         if_exist = select(cursor, ['video_id'], 'video_label', ' where video_id = %s' % k)
    #         if len(if_exist[1]) >= 1:
    #             update(cursor, ['label', 'create_time'], 'video_label', [str(v), now_time],
    #                    ' where video_id = %s' % k)
    #         else:
    #             insert(cursor, 'video_label', ['video_id', 'label', 'create_time'], [k, str(v), now_time])
    #     db.commit()

    def __init__(self, host=db_host, username=db_user, password=db_passwd, database=db_database, port=db_port):
        self.host = host
        self.port = port
        self.username = username
        self.password = password
        self.database = database

    def __enter__(self, ):
        self.db = pymysql.connect(host=self.host, user=self.username, password=self.password, database=self.database,
                                  port=int(self.port))
        self.cursor = self.db.cursor()

        return [self.db, self.cursor]

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.db.close()
        self.cursor.close()
        print("DATABASE CLOSED")


# inputs:
#   cursor: the cursor of database.
#   table_name: the name of insert table.
#   fields: the name of field.
#   parameters: a list of parameter.
#   using_text: using text sql to insert
# NOTE: user should commit the changes outside this function using db.commit()
def insert(cursor, table_name, fields, parameters, using_text=False, see_print=False):
    if len(fields) != len(parameters):
        raise Exception("The length of fields and parameters must be the same!")
    fields = ["`%s`" % (field) for field in fields]

    if using_text:
        values = []
        for i, parameter in enumerate(parameters):
            if type(parameter) == str:
                values.append("'" + parameter + "'")
            elif type(parameter) == int:
                values.append("" + str(parameter) + "")
            else:
                raise Exception(
                    "INSERT only support int or string, here is %s, contact xiejiayu@4paradigm.com to extend the type" % (
                        type(parameter)))

        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ','.join(fields), ','.join(values))
        if see_print: print(sql)
        return cursor.execute(sql)
    else:
        values = []
        for i, parameter in enumerate(parameters):
            if type(parameter) == str:
                values.append("%s")
            elif type(parameter) == int or type(parameter) == float:
                values.append("%s")
            else:
                print(parameters)
                raise Exception(
                    "INSERT only support int or string, here is %s, contact xiejiayu@4paradigm.com to extend the type" % (
                        type(parameter)))

        sql = "INSERT INTO %s (%s) VALUES (%s)" % (table_name, ','.join(fields), ','.join(values))
        if see_print:  print(sql, parameters)
        cursor.execute(sql, parameters)
        return cursor.lastrowid


def select(cursor, fields, table_names, condition=None, see_print=False):
    print_fields = ",".join(fields)
    if condition:
        sql = "SELECT %s FROM %s %s" % (print_fields, table_names, condition)
    else:
        sql = "SELECT %s FROM %s" % (print_fields, table_names)
    if see_print: print(sql)
    selected_number = cursor.execute(sql)
    return selected_number, cursor.fetchall()


def execute_select_sql(cursor, sql, see_print=False):
    if see_print: print(sql)
    selected_number = cursor.execute(sql)
    return selected_number, cursor.fetchall()


def excute_view_sql(cursor, table_name, sql, see_print=False):
    sql = "create or replace view %s as %s" % (table_name, sql)
    if see_print: print(sql)
    return cursor.execute(sql)


def create_tmp_sql(cursor, table_name, sql, see_print=False):
    sql = "create TEMPORARY table %s as %s" % (table_name, sql)
    if see_print: print(sql)
    return cursor.execute(sql)


# inputs:
#   cursor: the cursor of database.
#   table_name: the name of create table.
#   fields: the name of field.
#   field_types: a list of the type of fields.
#   extra_info:
# NOTE: user should commit the changes outside this function using db.commit()
def create_table(cursor, table_name, fields, field_types, extra_info=None, see_print=False):
    if len(fields) != len(field_types):
        raise Exception("The length of fields and field_types must be the same!")

    content = []
    for filed, field_type in zip(fields, field_types):
        content.append(filed + " " + field_type)
    if extra_info:
        content.append(extra_info)
    sql = "CREATE TABLE IF NOT EXISTS  %s (%s) ENGINE=InnoDB DEFAULT CHARSET=utf8;" % (table_name, ','.join(content))
    if see_print: print(sql)
    return cursor.execute(sql)


# db = connect_to_database()
# cursor = db.cursor()
# insert(cursor,"t1",["field1","field2","field3"],[3,"ccc","bbb"],see_print = True)
# create_table(cursor,"RE_doc",["doc_id","doc_state","doc_path"],["VARCHAR(255)","VARCHAR(255)","TEXT"],see_print=True)
# db.commiwt()

def update(cursor, fields, table_names, parameters, condition=None, see_print=False):
    if len(fields) != len(parameters):
        raise Exception("The length of fields and parameters must be the same!")

    update_set = []
    for filed, p_single in zip(fields, parameters):
        if type(p_single) == str:
            update_set.append("%s = '%s'" % (filed, p_single.replace("\'", "\\'")))
        elif type(p_single) == int:
            update_set.append("%s = %s" % (filed, p_single))
    update_set = ','.join(update_set)
    if condition:
        sql = "UPDATE %s SET %s %s" % (table_names, update_set, condition)
    else:
        sql = "UPDATE %s SET %s" % (table_names, update_set)
    if see_print: print(sql)
    return cursor.execute(sql)


def insert_many(cursor, table_name, fields, parameters_list, see_print=False):
    values_list = []
    insert_parameters = []
    fields = ["`%s`" % (field) for field in fields]

    for parameters in parameters_list:
        values = []
        for i, parameter in enumerate(parameters):
            if type(parameter) == str:
                values.append("%s")
            elif type(parameter) == int or type(parameter) == float:
                values.append("%s")
            else:
                print(parameters)
                raise Exception(
                    "INSERT only support int or string, here is %s, to extend the type" % (
                        type(parameter)))
        values_list.append("(" + ','.join(values) + ")")
        insert_parameters += parameters

    sql = "INSERT INTO %s (%s) VALUES %s" % (table_name, ','.join(fields), ','.join(values_list))
    if see_print:  print(sql, insert_parameters)
    return cursor.execute(sql, insert_parameters)
