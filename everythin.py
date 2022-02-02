from bs4 import BeautifulSoup
import requests
import re


url = "https://www.imdb.com/chart/toptv/?sort=rk,asc&mode=simple&page=1"
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')

querystring = {"page_size":"50"}
headers = {
    'x-rapidapi-host': "data-imdb1.p.rapidapi.com",
    'x-rapidapi-key': "199a887ebbmsh411d53cae20ce57p1f09fbjsn5e2e6c12f2f1"
    }
responses = []

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)

shows = soup.select('td.titleColumn')
links = [a.attrs.get('href') for a in soup.select('td.titleColumn a')]
crew = [a.attrs.get('title') for a in soup.select('td.titleColumn a')]
ratings = [b.attrs.get('data-value') for b in soup.select('td.posterColumn span[name=ir]')]
votes = [b.attrs.get('data-value') for b in soup.select('td.ratingColumn strong')]

list = []

for index in range(0, len(shows)):
    show_details = shows[index].get_text()
    show = (' '.join(show_details.split()).replace('.', ''))
    show_name = show[len(str(index)) + 1:-7]
    year = re.search('\((.*?)\)', show_details).group(1)
    place = show[:len(str(index)) - (len(show))]

    data = {"Shows Name": show_name,
            "year": year,
            "place": place,
            "Casting Group": crew[index],
            "rating": ratings[index],
            "vote": votes[index],
            "link": links[index]}
    list.append(data)

for show in list:
    f = open('txt files/top250.txt', 'a')
    print(show['place'], '-', show['Shows Name'], '(' + show['year'] +
          ') -', 'Starring:', show['Casting Group'], show['rating'], file=f)


lines = [0, 49, 99, 199]
i = 0
with open("txt files/top250.txt", "r") as input:
    with open("txt files/ratings.txt", "w") as output:
        for line in input:
            if i in lines:
                output.write(line)
            i += 1