import requests
import secrets
import json
import pandas as pd



def main():
    loc = f"https://imdb-api.com/en/API/UserRatings/{secrets.secret_key}/tt0331080"
    results = requests.get(loc)
    if results.status_code != 200:
        print("help!")
        return
    data = results.json()
    print(data)

    json_objects = json.dumps(data, indent=4)
    with open('wheelOfTime.json', 'w') as outfile:
        outfile.write(json_objects)

def jsonTOText():
    df = pd.read_json(r'wheelOfTime.json')
    df.to_csv (r'moviesFiles.txt', index=False)


class searchTitles:
    # Press the green button in the gutter to run the script.
    if __name__ == '__main__':
        main()
        jsonTOText()
