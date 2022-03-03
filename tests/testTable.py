import matplotlib.pyplot as plt
import userInterface

def test_graphs():
    data_results = userInterface.rankMovieGraph()
    assert len(data_results) == 250

def test_show_graph():
    data_results = userInterface.rankShowGraphh()
    assert len(data_results) == 250
