import parser
import sqlite3
import time
import datetime
import random
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from dateutil import parser
from matplotlib import style

style.use('fivethirtyeight')

from matplotlib import pyplot as plt

conn = sqlite3.connect('project1db.sqlite')
c = conn.cursor()


def read_from_db(db_cursor: sqlite3.Cursor):
    db_cursor.execute('SELECT * FROM  most_popular_movies')
    data = db_cursor.fetchall()
    print(data)
    for row in data:
        print(data)

    db_cursor.execute('SELECT * FROM  most_popular_movies WHERE rankchange = 3')
    data = db_cursor.fetchall()
    print(data)
    for row in data:
        print(row)

    db_cursor.execute('SELECT * FROM most_popular_movies WHERE ttid')
    data = db_cursor.fetchall()
    print(data)
    for row in data:
        print(row)

    db_cursor.execute('SELECT ttid, rankchange FROM most_popular_movies ')
    data = db_cursor.fetchall()
    print(data)
    for row in data:
        print(row[0])


read_from_db(c)
c.close()
conn.close()


def graph_data():
    c.execute('SELECT rankchange, value FROM most_popular_movies')
    data = c.fetchall()

    dates = []
    values = []

    for row in data:
        dates.append(parser.parse(row[0]))
        values.append(row[1])

    plt.plot_date(dates, values, '-')
    plt.show()
