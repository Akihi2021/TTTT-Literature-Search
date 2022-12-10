from helper import sql

if __name__ == "__main__":
    with sql.Db_connection() as [db, cursor]:
        num, user = sql.select(cursor, '*', 'user', "where id = %d" % 1)
        print(num) # result num
        print(user) # [{}, {}]
        db.commit()
