from helper import sql
import datetime


def do_comment(user_id, paper_id, content):
    with sql.Db_connection() as [db, cursor]:
        time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        sql.insert(cursor, 'comment', [
            'user_id', 'paper_id', 'content', 'time'], [user_id, paper_id, content, time])

        db.commit()

        return True


def get_comment(paper_id):
    with sql.Db_connection() as [db, cursor]:
        num, comments = sql.select(cursor,
                                   '*',
                                   'comment',
                                   "where paper_id = '%s'" % paper_id)

        return comments



