import sqlite3


def open_dbase(fileName: str) -> tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(fileName)  # connects to DB
    cursor = db_connection.cursor()  # preps to raed/write data
    return db_connection, cursor


def close_dbase(connection: sqlite3.Connection):
    connection.commit()  # saves any changes
    connection.close()


def save_to_dbase(db_table, datafile):
    with sqlite3.connect("db.sqlite3") as conn:
        command = "INSERT INTO" + db_table + "VALUES (?,?,?,?,?,?,?)"
        for data in datafile:
            conn.execute(command, tuple(data.values()))
        conn.commit()


def save_ratings_to_dbase(db_table, datafile):
    with sqlite3.connect("db.sqlite3") as conn:
        command = "INSERT INTO" + db_table + " VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
        for data in datafile:
            conn.execute(command, data)
        conn.commit()


def get_from_dbase(db_table):
    with sqlite3.connect("db.sqlite3") as conn:
        command = "SELECT * FROM " + db_table
        cursor = conn.execute(command)
        results = cursor.fetchall()
        return results

def main():
    conn, cursor = open_dbase("imdbShow_db.sqlite")
    print(type(conn))
    close_dbase(conn)
if __name__ == '__main__':
    main()