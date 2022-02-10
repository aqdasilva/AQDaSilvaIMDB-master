import json
import sqlite3
import sys
from typing import Tuple
import requests
import secrets

db = sqlite3.connect('showData.sqlite', timeout=10)
cursor = db.cursor()


def get_top_250_data() -> list[dict]:
    api_query = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secret_key}"
    response = requests.get(api_query)
    if response.status_code != 200:  # if we don't get an ok response we have trouble
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)
    # jsonresponse is a kinda useless dictionary, but the items element has what we need
    jsonresponse = response.json()
    show_list = jsonresponse["items"]
    return show_list


filename = "data.json"


# def remove_punc(string):
#   punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
#   for ele in string:
#      if ele in punc:
#         string = string.replace(ele, "")
# return string


# try:
#   with open(filename, 'r', encoding="utf-8") as f:
#      data = f.read()
# with open(filename, "w+", encoding="utf-8") as f:
#    f.write(remove_punc(data))
#  print("Removed punctuations from the file", filename)
# except FileNotFoundError:
#   print("File not found")


def report_results(data_to_write: list[dict]):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def get_ratings(top_show_data: list[dict]) -> list[dict]:
    results = []
    api_queries = []
    base_query = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/"
    wheel_of_time_query = f"{base_query}tt7462410"
    api_queries.append(wheel_of_time_query)
    first_query = f"{base_query}{top_show_data[0]['id']}"
    api_queries.append(first_query)
    fifty_query = f"{base_query}{top_show_data[49]['id']}"
    api_queries.append(fifty_query)
    hundred_query = f"{base_query}{top_show_data[99]['id']}"
    api_queries.append(hundred_query)
    two_hundered = f"{base_query}{top_show_data[199]['id']}"
    api_queries.append(two_hundered)
    for query in api_queries:
        response = requests.get(query)
        if response.status_code != 200:  # if we don't get an ok response we have trouble, skip it
            print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
            continue
        rating_data = response.json()
        results.append(rating_data)
    return results


def create_dbase(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    conn = sqlite3.connect('showData.sqlite')
    conn.cursor()

    cursor.execute('''CREATE TABLE IF NOT EXISTS showRatings(
 id TEXT,
 title TEXT NULL,
 fulltitle TEXT NULL,
 year TEXT ,
 crew TEXT,
 imDbRating TEXT,
 imDbRatingCount TEXT,
 PRIMARY KEY (id)
 );''')

    cursor.execute('''CREATE TABLE IF NOT EXISTS userRatings(
imdbid INTEGER NOT NULL,
totalRating TEXT,
totalRatingVotes TEXT,
TenRating_Perc FLOAT NOT NULL,
TenRatingVotes INTEGER NOT NULL,
NineRating_perc FLOAT NOT NULL,
NineRatingVotes INTEGER NOT NULL,
EightRating_perc FLOAT NOT NULL,
EightRatingVotes INTEGER NOT NULL,
SevenRating_perc FLOAT NOT NULL,
SevenRatingVotes INTEGER NOT NULL,
SixRating_perc FLOAT NOT NULL,
SixRatingVotes INTEGER NOT NULL,
FiveRating_perc FLOAT NOT NULL,
FiveRatingVotes INTEGER NOT NULL,
FourRating_perc FLOAT NOT NULL,
FourRatingVotes INTEGER NOT NULL,
ThreeRating_perc FLOAT NOT NULL,
ThreeRatingVotes INTEGER NOT NULL,
TwoRating_Perc FLOAT NOT NULL,
TwoRatingVotes INTEGER NOT NULL,
OneRating_perc FLOAT NOT NULL,
OneRatingVotes INTEGER NOT NULL,
FOREIGN KEY (imdbid) REFERENCES showRatings(id)
 );''')

    conn.commit()
    conn.close()


def insert_data(cursor: sqlite3.Cursor):
    loc = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/"
    results = requests.get(loc)
    data = results.json()
    # connects
    conn = sqlite3.connect('showData.sqlite')
    # creates cursor
    conn.cursor()

    for i in range(0, 250):  ## gets id 1 thru 250, all 7 items
        cursor.execute('''INSERT INTO showRatings(Id, title, fulltitle, year, crew, imDbRating, imDbRatingCount)
            VALUES (?,?,?,?,?,?,?)''',
                       (data['items'][i]['id'], data['items'][i]['title'],
                        data['items'][i]['fullTitle'], data['items'][i]['year'],
                        data['items'][i]['crew'], data['items'][i]['imDbRating'],
                        data['items'][i]['imDbRatingCount']))

    cursor.execute('SELECT * FROM showRatings')
    conn.commit()
    conn.close()
    # 'imDbId', 'title', 'fullTitle', 'year', 'crew', 'imDbRating', 'imDbRatingCount'
    # %s,%s,%s,%s,%s,%s,%s
    # cursor.execute('SELECT * FROM showRatings')
    # conn.commit()


def get_user_ratings(cursor: sqlite3.Cursor, user_ratings: list[dict]) -> list[dict]:
    loc = f"https://imdb-api.com/en/API/Top250TVs/k_09bvlwau"
    results = requests.get(loc)
    data = results.json()
    conn = sqlite3.connect('showData.sqlite')
    conn.cursor()
    results = []
    api_queries = []
    wheel_of_time_query = f"{loc}tt7462410"
    api_queries.append(wheel_of_time_query)
    first_query = f"{loc}{user_ratings[0]['id']}"
    api_queries.append(first_query)
    fifty_query = f"{loc}{user_ratings[49]['id']}"
    api_queries.append(fifty_query)
    hundred_query = f"{loc}{user_ratings[99]['id']}"
    api_queries.append(hundred_query)
    two_hundered = f"{loc}{user_ratings[199]['id']}"
    api_queries.append(two_hundered)

    for i in list(0, 49, 99, 199):
        cursor.execute('''INSERT INTO userRatings(imdbid,
totalRating,
totalRatingVotes,
TenRating_Perc,
TenRatingVotes,
NineRating_perc,
NineRatingVotes,
EightRating_perc,
EightRatingVotes,
SevenRating_perc,
SevenRatingVotes,
SixRating_perc,
SixRatingVotes,
FiveRating_perc,
FiveRatingVotes,
FourRating_perc,
FourRatingVotes,
ThreeRating_perc,
ThreeRatingVotes,
TwoRating_Perc,
TwoRatingVotes,
OneRating_perc,
OneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''')


def main():
    conn, cursor = create_dbase("showData.sqlite")
    conn = sqlite3.connect("showData.sqlite")
    setup_db(cursor)
    insert_data(cursor)
    # top_show_data = get_top_250_data()
    # ratings_data = get_ratings(top_show_data)
    # remove_punc(filename)
    # report_results(ratings_data)
    # report_results(top_show_data)
    close_db(conn)


if __name__ == '__main__':
    main()
