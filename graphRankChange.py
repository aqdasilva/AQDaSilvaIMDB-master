import matplotlib.pyplot as plt
import np
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
import tkinter as tk
from tkinter import *

class Root(tk.Tk):
    def __init__(self):
        super(Root, self).__init__()
        self.title("Movies")
        self.rankMovieGraph()



    def graphToCanvasGUI(self):

        f = Figure(figsize=(5, 5), dpi=100)
        data = f.add_subplot(rankMovieGraph)
        data.plot
        canvas = FigureCanvasTkAgg(f, self)
        canvas.draw()

        canvas.get_tk_widget().pack(side=BOTTOM, fill=BOTH, expand=True)

class rankMovieGraph():
            x = []
            y = []

            with open('csv/movies/most_popular_movies.csv', 'r') as csvfile:
                plots = np.loadtxt(csvfile, delimiter=',', skiprows=1, usecols=range(1, 3))

                for row in plots:
                    x.append(row[0])
                    y.append(int(row[1]))

            plt.bar(x, y, color='g', width=0.50, label="Rank(+/-)")

            plt.xlabel('Rank')
            plt.ylabel('Rank Change')
            plt.title('Movie Changes', fontsize=20)


            plt.legend()
            plt.show()

class rankShowGraph():
    x = []
    y = []

    with open('csv/shows/most_popular_shows.csv', 'r') as csvfile:
        plots = np.loadtxt(csvfile, delimiter=',', skiprows=1, usecols=range(1, 3))

        for row in plots:
            x.append(row[0])
            y.append(int(row[1]))

    plt.bar(x, y, color='g', width=0.50, label="Rank(+/-)")

    plt.xlabel('Rank')
    plt.ylabel('Rank Change')
    plt.title('Show Changes', fontsize=20)

    plt.legend()
    plt.show()



