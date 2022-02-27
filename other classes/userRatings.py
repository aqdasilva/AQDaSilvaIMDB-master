import requests
import secrets
import json
import pandas as pd


def main():
    loc = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt5491994"  # 1
    loc2 = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt0081834"  # 50
    loc3 = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt0096697"  # 100
    loc4 = f"https://imdb-api.com/en/API/UserRatings/k_09bvlwau/tt2100976"  # 200

    results = requests.get(loc)
    results2 = requests.get(loc2)
    results3 = requests.get(loc3)
    results4 = requests.get(loc4)

    if results.status_code != 200:
        print("help!")
        return
    data1 = results.json()
    print(data1)

    if results2.status_code != 200:
        print("help!")
        return
    data2 = results2.json()
    print(data2)

    if results3.status_code != 200:
        print("help!")
        return
    data3 = results3.json()
    print(data3)

    if results4.status_code != 200:
        print("help!")
        return
    data4 = results4.json()
    print(data4)

    data = (data1, data2, data3, data4)

    json_objects = json.dumps(data, indent=4)
    with open('../json/ratings.json', 'w') as outfile:
        outfile.write(json_objects)

def toTextFile():
    df = pd.read_json(r'../json/ratings.json')
    df.to_csv (r'ratings.txt', index=False)



class ratings:
    # Press the green button in the gutter to run the script.
    if __name__ == '__main__':
        main()
        toTextFile()

