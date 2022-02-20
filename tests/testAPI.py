import api_grabs


def test_gettop250():
    top250_results = api_grabs.get_top_250_data()
    assert len(top250_results) == 250

