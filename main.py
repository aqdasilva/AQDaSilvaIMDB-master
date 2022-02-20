import api_grabs
import dbase


def report_results(data_to_write: list):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def main():
    connection, db_cursor = dbase.open_db("project1db.sqlite")
    dbase.create_top250_table(db_cursor)
    dbase.create_ratings_table(db_cursor)
    dbase.create_popular_table(db_cursor)
    dbase.create_popular_movie_table(db_cursor)
    dbase.create_movie_table(db_cursor)
    dbase.create_change_movies(db_cursor)

    top_show_data = api_grabs.get_top_250_data()
    top_show_data_for_db = api_grabs.prepare_top_250_data(top_show_data)

    popular_show_data = api_grabs.get_popular_shows()
    popular_show_for_db = api_grabs.prepare_popular_movies_data(popular_show_data)

    top_movie_data = api_grabs.get_top_movies()
    top_movies_for_db = api_grabs.prepare_top_movies_for_db(top_movie_data)

    popular_movie_data = api_grabs.get_popular_movies()
    popular_movie_for_db = api_grabs.prepare_popular_shows_for_db(popular_movie_data)



    dbase.insert_top_shows_dbase(top_show_data_for_db, db_cursor)
    dbase.insert_wheel_of_time_into_dbase(db_cursor)
    dbase.insert_popular_shows(popular_show_for_db, db_cursor)
    dbase.insert_top_movies(top_movies_for_db, db_cursor)
    dbase.insert_popular_movies(popular_movie_for_db, db_cursor)

    dbase.get_neg_3_movies(db_cursor)
    dbase.get_top_3_movies(db_cursor)


    ratings_data = api_grabs.get_ratings(top_show_data)
    db_ready_ratings_data = api_grabs.prepare_ratings_for_db(ratings_data)
    dbase.insert_ratings_into_dbase(db_ready_ratings_data, db_cursor)




    dbase.close_db(connection)


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