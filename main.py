import PySide6

import api_grabs
import dbase
import sqlite3
import SecondWindow
import GUIWindow
import sys
from graphRankChange import rankMovieGraph,rankShowGraph
import openpyxl
import userInterface


def report_results(data_to_write: list):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def get_data_and_put_in_db(db_cursor: sqlite3.Cursor):
    top_show_data = api_grabs.get_top_250_data("TV")
    top_movie_data = api_grabs.get_top_250_data("Movie")
    top_show_data_for_db = api_grabs.prepare_top_250_data(top_show_data)
    top_movie_data_for_db = api_grabs.prepare_top_250_data(top_movie_data)
    most_pop_movies = api_grabs.get_most_popular("Movies")
    most_pop_tv = api_grabs.get_most_popular("TVs")
    # I'm getting sloppy here to make this quicker and the code smaller
    dbase.put_top_250_in_database("top_show_data", top_show_data_for_db, db_cursor)
    dbase.put_top_250_in_database("top_movie_data", top_movie_data_for_db, db_cursor)
    dbase.put_most_popular_in_database("most_popular_movies", most_pop_movies, db_cursor)
    dbase.put_most_popular_in_database("most_popular_shows", most_pop_tv, db_cursor)
    dbase.put_in_wheel_of_time(db_cursor)
    big_mover_records = api_grabs.get_big_movers(most_pop_movies)
    big_mover_ratings = api_grabs.get_big_mover_ratings(big_mover_records)
    ratings_data = api_grabs.get_ratings(top_show_data)
    db_ready_ratings_data = api_grabs.prepare_ratings_for_db(ratings_data)
    dbase.put_ratings_into_db(db_ready_ratings_data, db_cursor)
    dbase.put_ratings_into_db(big_mover_ratings, db_cursor)

def GUI_data(data:list):
    qt_app = PySide6.QtWidgets.QApplication(sys.argv)  # sys.argv is the list of command line arguments
    my_window = GUIWindow.DataWindows(data)
    sys.exit(qt_app.exec())

def getAllRankChange()-> list[dict]:
    open


def main():
    connection, db_cursor = dbase.open_db("project1db.sqlite")
    dbase.create_all_tables(db_cursor)
    get_data_and_put_in_db(db_cursor)
    dbase.close_db(connection)
    GUI_data(getAllRankChange())
    userInterface()


if __name__ == '__main__':
    main()


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
