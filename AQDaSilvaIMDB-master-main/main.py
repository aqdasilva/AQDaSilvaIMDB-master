import pandas as pd, requests, responses, secrets, json, sqlite3, sys
from pathlib import Path
from typing import Tuple



def getTop250() -> list[dict]:
    api_query = f"https://imdb-api.com/en/API/Top250TVs/k_09bvlwau"
    results = requests.get(api_query)

    if results.status_code != 200:
        print(f"major help !:{results.status_code} & Error Message:{results.reason} ")
        sys.exit(-1)

    jsonresponse = results.json()
    shows_list = jsonresponse["items"]
    return shows_list

def output(date_to_write: list[dict]):
    with open("top250.txt", mode='a') as outputFile:
        for show in date_to_write:
            print(show, file=outputFile)
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)

def userRatings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_que = []
    base_que = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/"
    wheel_show_que = f"{base_que}tt7462410"
    api_que.append(wheel_show_que)
    first_query = f"{base_que}{top_show_data[0]['id']}"
    api_que.append(first_query)
    fifty_query = f"{base_que}{top_show_data[49]['id']}"
    api_que.append(fifty_query)
    hundred_query = f"{base_que}{top_show_data[99]['id']}"
    api_que.append(hundred_query)
    two_hundered = f"{base_que}{top_show_data[199]['id']}"
    api_que.append(two_hundered)

    for query in api_que:
        response = requests.get(query)
        if response.status_code != 200:
            print(f"failed to get data, code{response.status_code} and error message{response.reason}")
            continue
        ratting_data = response.json()
        results.append(ratting_data)
    return results

def open_dbase(fileName:str) ->tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(fileName)#connects to DB
    cursor = db_connection.cursor() #preps to raed/write data
    return db_connection, cursor

def close_dbase(connection:sqlite3.Connection):
    connection.commit() #saves any changes
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

def add_shows2_DBase(self):
    try:
        self.cursor.execute("""INSERT INTO showData (#######/////) VALUES
        (?,?,?,?,?,?,?)""",(getTop250(), output()))
        query = f"""SELECT * FROM showData"""
        self.cursor.execute(query)
        df = pd.DataFrame.from_records(self.cursor.fetchall())
        print(df)
    except Exception as e:
        self.duplicate_entry.exec()
        print(Exception, e)




def main():
    top250 = getTop250()
    ratings_data = userRatings(top250)
    output(ratings_data)
    output(top250)

    conn, cursor = open_dbase("imdbShow_db.sqlite")
    print(type(conn))
    conno = sqlite3.connect('imdbShow_db.sqlite')
    cursor = conno.cursor()
    shows250 = getTop250()
    shows250.append(cursor)





if __name__ == '__main__':
    main()

