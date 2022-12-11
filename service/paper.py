from helper import sql
import datetime


def comment(user_id, paper_id, content):
    with sql.Db_connection() as [db, cursor]:
        time = datetime.dateime.now().strftime("%Y-%m-%d %H:%M:%S")
        success = sql.insert(cursor, 'comment', [
            'user_id', 'paper_id', 'content', 'time'], [user_id, paper_id, content, time])
        db.commit()

        return success == 1


