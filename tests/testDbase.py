import dbase

# we'll save this one for the next tests
def test_data_entries():
    test_api_data_entry = [{"id": "tttestdata", "rank": "10002", "rankUpDown": "+4000", "title": "Comp490 Project 1 Show",
                        "fullTitle": "Comp490 Project 1 Show (2022)", "year": "2022", "image": "",
                        "crew": "Prof. Santore and many hardworking students", "imDbRating": "9.2",
                        "imDbRatingCount": "41"}]
    return test_api_data_entry

def get_database():
    conn, cursor = dbase.open_db("project1db.sqlite")
    return conn, cursor

# test here actually showed me a hidden error in my database
def test_enter_data():
    # I should really do some of this in a fixture, but I wanted to do it with just what you already have
    # the database needs to be deleted everytime to make this test run, which is good for github actions
    test_data_entry = [("tttestdata", 10002, "Comp490 Project 1 Show", "Comp490 Project 1 Show (2022)", 2022,
                        "", "Prof. Santore and many hardworking students", 9.2, 41)]

    connection, db_cursor = dbase.open_db("project1db.sqlite")
    dbase.create_top250_table(db_cursor)
    dbase.put_top_250_in_database(test_data_entry, db_cursor)
    connection.commit()
    # this test in the next four lines wasn't technically required, but I wanted to demo the count feature
    # and it is a good idea. I could test by checking the len of record_count_set also
    db_cursor.execute("SELECT COUNT() FROM top_show_data WHERE ttid = 'tttestdata'")
    record_count_set = db_cursor.fetchone()
    number_of_records = record_count_set[0]  # the count returns a tuple, the count is the first element
    assert number_of_records == 1
    db_cursor.execute("SELECT * FROM top_show_data WHERE ttid = 'tttestdata'")
    record_set = db_cursor.fetchall()
    assert record_set[0] == test_data_entry[0]

def test_enter_mover_movies():
    test_data_entry = [("tttestdata", 10002, "+40000" "Comp490 Project 1 Show", "Comp490 Project 1 Show (2022)", 2022,
                        "", "Prof. Santore and many hardworking students", 9.2, 41)]

    connection, db_cursor = dbase.open_db("project1db.sqlite")
    dbase.create_change_movies(db_cursor)
    dbase.get_top_3_movies(test_data_entry, db_cursor)
    connection.commit()

    db_cursor.execute("SELECT COUNT() FROM popular_movies WHERE ttid = 'tttestdata'")
    record_count_set = db_cursor.fetchone()
    number_of_records = record_count_set[0]
    assert number_of_records == 3
    db_cursor.execute("SELECT * FROM popular_movies WHERE ttid = 'tttestdata'")
    record_set = db_cursor.fetchall()
    assert record_set[0] == test_data_entry[0]

    ##similar to sprint2 test, using fake/real data to write into the database bringing back the positive and negative top 3 mover from popular movies data.

def test_popular_movies_table(get_db, test_data_entries):
    conn, cursor = get_db
    test_dict = test_data_entries
    dbase.insert_popular_movies(cursor, test_dict)
    cursor.execute('''SELECT ttid FROM sqlite_master WHERE type = 'table' and ttid LIKE 'title_%'; ''')
    results = cursor.fetchall()
    assert len(results) == 1
    cursor.execute('''SELECT ttid FROM sqlite_master WHERE type ='table' AND ttid 'rankUpDown_%';''')
    results = cursor.fetchall()
    assert len(results) == 1
    ##### this will inout data into the new table , ensuring the new table has been made.
    ### fetches the table for the popular movies with the title and rnakUpDown columns


def _write_to_popular_movies():




