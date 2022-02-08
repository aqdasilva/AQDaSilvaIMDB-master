import json
import sqlite3
import sys
from typing import Tuple
import requests
import secrets
import urllib.request
from os import path

# comment to test workflow is there a github actions workflow?
db = sqlite3.connect('showData.db')
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


filename = "Output.txt"


#def remove_punc(string):
#   punc = '''!()-[]{};:'"\, <>./?@#$%^&*_~'''
 #   for ele in string:
  #      if ele in punc:
   #         string = string.replace(ele, "")
   # return string


#try:
 #   with open(filename, 'r', encoding="utf-8") as f:
  #      data = f.read()
   # with open(filename, "w+", encoding="utf-8") as f:
    #    f.write(remove_punc(data))
  #  print("Removed punctuations from the file", filename)
#except FileNotFoundError:
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
    base_query = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/"
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

def create_dbase(filename:str) ->Tuple[sqlite3.Connection, sqlite3.Cursor]:
    db_connection = sqlite3.connect(filename)#connect to existing DB or create new one
    cursor = db_connection.cursor()#get ready to read/write data
    return db_connection, cursor

def close_db(connection:sqlite3.Connection):
    connection.commit()#make sure any changes get saved
    connection.close()

def setup_db(cursor:sqlite3.Cursor):
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
imdbId INTEGER PRIMARY KEY,
totalRating INTEGER,
totalRatingVotes INTEGER,
TenRating INTEGER,
TenRatingVotes INTEGER 
 );''')

#def insert_data(cursor:sqlite3.Cursor):
 #   cursor.execute(f'''INSERT INTO showData(id, title, fulltitle, year, crew)
  #                  VALUES ('imDbId', 'title', 'fullTitle', 'year', 'crew',{####make function in here})''')







def main():
    conn, cursor = create_dbase("showData.sqlite")
    print(type(conn))
   #close_db(conn)
    setup_db(conn)

    top_show_data = get_top_250_data()
    ratings_data = get_ratings(top_show_data)
   # remove_punc(filename)
    report_results(ratings_data)
    report_results(top_show_data)

if __name__ == '__main__':
    main() in ()
