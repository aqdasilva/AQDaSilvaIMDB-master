import pytest

import json
import sqlite3
import sys
from typing import Tuple
import requests
import secrets
import urllib.request
from os import path

db = sqlite3.connect('showData.sqlite')
cursor = db.cursor()


def get_top_250_data() -> list[dict]:
    api_query = f"https://imdb-api.com/en/API/Top250TVs/k_09bvlwau"
    response = requests.get(api_query)
    if response.status_code != 200:  # if we don't get an ok response we have trouble
        print(f"Failed to get data, response code:{response.status_code} and error message: {response.reason} ")
        sys.exit(-1)
    # jsonresponse is a kinda useless dictionary, but the items element has what we need
    jsonresponse = response.json()
    show_list = jsonresponse["items"]
    return show_list


filename = "showData.sqlite"


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
    wheel_of_time_query = f"{base_query}z"
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


def open_dbase(filename: str) -> Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)  # connect to existing DB or create new one
    cursor = db_connection.cursor()  # get ready to read/write data
    return db_connection, cursor


def close_db(connection: sqlite3.Connection):
    connection.commit()  # make sure any changes get saved
    connection.close()


def setup_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS showRatings(
 id INTEGER PRIMARY KEY,
 title TEXT NOT NULL,
 fulltitle TEXT NOT NULL,
 year INTEGER ,
 crew TEXT,
 imDbRating INTEGER,
 imDbRatingCount INTEGER
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


#cursor.execute('''DROPS TABLE if showRatings''')


def insert_data(cursor: sqlite3.Cursor):
    loc = f"https://imdb-api.com/en/API/Top250TVs/k_09bvlwau"
    results = requests.get(loc)
    data = results.json()
    conn = sqlite3.connect('showData.sqlite')
    conn.cursor()
    for i in range(0, 250):
        cursor.execute(f'''INSERT INTO showRatings(id, title, fulltitle, year, crew, imDbRating, imdbRatingCount)
                 VALUES (?,?,?,?,?,?,?)''',
                       (data['items'][i]['id'], data['items'][i]['title'], data['items'][i]['fullTitle'],
                        data['items'][i]['year'], data['items'][i]['crew'], data['items'][i]['imDbRating'],
                        data['items'][i]['imDbRatingCount']))

    cursor.execute('SELECT * FROM showRatings')
    conn.commit()
    conn.close()

def insert_data_table_two(cursor: sqlite3.Cursor):
    loc1 = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt5491994"
    loc2 = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt0081834"
    loc3 = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt0096697"
    loc4 = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt2100976"
    wheel_loc = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt7462410"
    results = requests.get(loc1, loc2, loc3, loc4, wheel_loc)
    data = results.json()
    conn = sqlite3.connect('showData.sqlite')
    conn.cursor()
    for i in data:
        cursor.execute(f'''INSERT INTO userRatings(imdbid,
totalRating,totalRatingVotes,TenRating_Perc,TenRatingVotes,NineRating_perc,NineRatingVotes,EightRating_perc,EightRatingVotes,
SevenRating_perc,SevenRatingVotes,SixRating_perc,SixRatingVotes,FiveRating_perc,FiveRatingVotes,FourRating_perc,FourRatingVotes,
ThreeRating_perc,ThreeRatingVotes,TwoRating_Perc,TwoRatingVotes ,OneRating_perc,OneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
        (data['imDbId'][i]['imdbid'], data['imDbId'][i]['totalRating'], data['imDbId'][i]['totalRatingVotes'], data['imDbId'][i]['TenRating_Perc'], data['imDbId'][i]['TenRatingVotes'], data['imDbId'][i]['NineRating_perc'], data['imDbId'][i]['NineRatingVotes'], data['imDbId'][i]['EightRating_perc'],
        data['imDbId'][i]['EightRatingVotes'], data['imDbId'][i]['SevenRating_perc'], data['imDbId'][i]['SevenRatingVotes'], data['imDbId'][i]['SixRating_perc'],data['imDbId'][i]['SixRatingVotes'], data['imDbId'][i]['FiveRating_perc'], data['imDbId'][i]['FiveRatingVotes'], data['imDbId'][i]['FourRating_perc'], data['imDbId'][i]['FourRatingVotes'],
        data['imDbId'][i]['FourRating_perc'], data['imDbId'][i]['FourRatingVotes'], data['imDbId'][i]['ThreeRating_perc'], data['imDbId'][i]['ThreeRatingVotes'], data['imDbId'][i]['TwoRating_Perc'], data['imDbId'][i]['TwoRatingVotes'],data['imDbId'][i]['OneRatingVotes'], data['imDbId'][i]['OneRatingVotes']))
    cursor.execute('SELECT * FROM userRatings')
    conn.commit()
    conn.close()




def main():
    conn, cursor = open_dbase("showData.sqlite")
    print(type(conn))
    setup_db(conn)
    insert_data(conn)
    insert_data_table_two(conn)
    top_show_data = get_top_250_data()
    ratings_data = get_ratings(top_show_data)
    # remove_punc(filename)
    report_results(ratings_data)
    report_results(top_show_data)

    close_db(conn)

if __name__ == '__main__':
    main() in ()
