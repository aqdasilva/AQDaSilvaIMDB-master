import requests
import secrets
import json
import pandas as pd


def main():
    loc = f"https://imdb-api.com/en/API/Top250TVs/{secrets.secret_key}"
    loc2 = f"https://imdb-api.com/api#UserRatings-header"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()
    print(data)

    json_objects = json.dumps(data, indent=4)
    with open('json/data.json', 'w') as outfile:
        outfile.write(json_objects)


def toTextFile():
    with open('json/data.json') as json_file:
        data = json.load(json_file)

        print(type[data])

        for key, value in data.items():
            print(f"\nKey: {key}")
            print(f"Value: {value}\n")

        json_file.close()

def jsonTOText():
    df = pd.read_json(r'json/data.json')
    df.to_csv (r'top250.txt', index=False)


class topTVs:
    # Press the green button in the gutter to run the script.
    if __name__ == '__main__':
        main()
        toTextFile()
        jsonTOText()
