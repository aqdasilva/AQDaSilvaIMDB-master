import sqlite3
from typing import Tuple

import requests
from pandas._testing import loc

db = sqlite3.connect('test_db.sqlite')
cursor = db.cursor()

def test_api_get():
    resp = requests.get(f"https://imdb-api.com/en/API/Top250TVs/k_09bvlwau")
    assert (resp.status_code == 200), "Status code is not 200. Rather found : " + str(resp.status_code)
    for record in resp.json()['data']:
        if record['id'] == 4:
            assert record['items'] == "id", \
                "NO data pulled from website Expected : found this though: " + str(record['items'])

def open_dbase(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()
def second_test(cursor: sqlite3.Cursor):
    dict = {
        "title": "Wheel of time "
    }
    cursor.execute('''CREATE TABLE IF NOT EXISTS thirdTable(
      id INTEGER PRIMARY KEY,
 title TEXT NOT NULL,
 fulltitle TEXT NOT NULL,
 year INTEGER ,
 crew TEXT,
 imDbRating INTEGER,
 imDbRatingCount INTEGER
 );''')

def insert_data_db(cursor: sqlite3.Cursor):
    loc = f"https://imdb-api.com/en/API/Top250TVs/k_09bvlwau"
    results = requests.get(loc)
    data = results.json()
    conn = sqlite3.connect('showData.sqlite')
    conn.cursor()
    for i in range(0, 250):
        cursor.execute(f'''INSERT INTO thirdTable(id, title, fulltitle, year, crew, imDbRating, imdbRatingCount)
                 VALUES (?,?,?,?,?,?,?)''',
                   (data['items'][i]['id'], data['items'][i]['title'], data['items'][i]['fullTitle'],
                    data['items'][i]['year'], data['items'][i]['crew'], data['items'][i]['imDbRating'],
                    data['items'][i]['imDbRatingCount']))

    cursor.execute('SELECT * FROM showRatings')
    conn.commit()
    conn.close()

def main():
    test_api_get(dict)
    conn, cursor = open_dbase()
    print(type(conn))
    second_test(conn)
    insert_data_db(conn)
    close_db(conn)

if __name__ == '__main__':
    main() in ()



