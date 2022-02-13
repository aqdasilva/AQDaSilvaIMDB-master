import sqlite3
from typing import Tuple


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
 rank INTEGER DEFAULT 0,
 title TEXT NOT NULL,
 fulltitle TEXT NOT NULL,
 year INTEGER ,
 image_url TEXT,
 crew TEXT,
 imDbRating INTEGER,
 imDbRatingCount INTEGER
 );''')

def setup_rating_db(cursor: sqlite3.Cursor):
    cursor.execute('''CREATE TABLE IF NOT EXISTS userRatings(
ratings_key INTEGER PRIMARY KEY,
imdb_ttcode TEXT NOT NULL,
title TEXT,
fulltitle TEXT,
year INTEGER ,
totalRating TEXT,
totalRatingVotes TEXT,
TenRating_Perc REAL,
TenRatingVotes INTEGER,
NineRating_perc REAL,
NineRatingVotes INTEGER,
EightRating_perc REAL,
EightRatingVotes INTEGER,
SevenRating_perc REAL,
SevenRatingVotes INTEGER,
SixRating_perc REAL,
SixRatingVotes INTEGER,
FiveRating_perc REAL,
FiveRatingVotes INTEGER,
FourRating_perc REAL,
FourRatingVotes INTEGER,
ThreeRating_perc REAL,
ThreeRatingVotes INTEGER,
TwoRating_Perc REAL,
TwoRatingVotes INTEGER,
OneRating_perc REAL,
OneRatingVotes INTEGER,
FOREIGN KEY (imdbid) REFERENCES showRatings(id) 
ON DELETE CASCADE ON UPDATE NO ACTION
 );''')


def insert_data(data_to_add: list[tuple], cursor: sqlite3.Cursor):
    cursor.executemany("""INSERT INTO showRatings(id, rank, title, fulltitle, year, image_url, crew, imDbRating, imDbRatingCount)
    VALUES(?,?,?,?,?,?,?,?,?)""", data_to_add)

def wheel_of_time_data(cursor: sqlite3.Cursor):
    cursor.execute("""INSERT INTO showRatings(id, title, fulltitle, year, crew, imDbRating, imDbRatingCount)
    VALUES('tt7462410',0,'The Wheel of Time','The Wheel of Time (TV Series 2021– )',2021,'','Rosamund Pike, Daniel Henney',
    7.2,85286)""")


def insert_data_table_two(data_to_add: list[tuple], cursor: sqlite3.Cursor):
    cursor.executemany(f'''INSERT INTO userRatings(imdbid,
totalRating,totalRatingVotes,TenRating_Perc,TenRatingVotes,NineRating_perc,NineRatingVotes,EightRating_perc,EightRatingVotes,
SevenRating_perc,SevenRatingVotes,SixRating_perc,SixRatingVotes,FiveRating_perc,FiveRatingVotes,FourRating_perc,FourRatingVotes,
ThreeRating_perc,ThreeRatingVotes,TwoRating_Perc,TwoRatingVotes ,OneRating_perc,OneRatingVotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''', data_to_add)

