import api_grabs
import dbase

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


def report_results(data_to_write: list):
    with open("Output.txt", mode='a') as outputFile:  # open the output file for appending
        for show in data_to_write:
            print(show, file=outputFile)  # write each data item to file
            print("\n", file=outputFile)
            print("===================================================================", file=outputFile)


def main():
    conn, cursor = dbase.open_dbase("showData.sqlite")
    dbase.setup_db(cursor)
    dbase.setup_rating_db(cursor)
    top_tv_shows = api_grabs.get_top_250_data()
    top_tv_shows_db = api_grabs.prepare_top_250_data(top_tv_shows)
    dbase.insert_data(top_tv_shows_db, cursor)
    dbase.wheel_of_time_data(cursor)
    ratings_data = api_grabs.get_ratings(top_tv_shows)
    db_ratings_data = api_grabs.prepare_ratings_for_db(ratings_data)
    dbase.insert_data_table_two(db_ratings_data, cursor)
    dbase.close_db(conn)

if __name__ == '__main__':
    main() in ()