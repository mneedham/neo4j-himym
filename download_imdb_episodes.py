import requests
from bs4 import BeautifulSoup
from soupselect import select
import cgi
import urlparse

pages = {}
for season in range(1, 10):
    episode_guide = open("data/season-" + str(season), 'r')
    soup = BeautifulSoup(episode_guide.read())

    for row in select(soup, "div.list_item"):
        episode_number = select(row, "div.image div div")[0].text
        uri = select(row, "div.info a")[0].get("href")
        pages[episode_number] = urlparse.urlparse(uri)[2]

for key, value in pages.iteritems():
    key = key.replace(", ", "-")
    filename = "imdb/" + key
    with open(filename, 'wb') as handle:
        file = "http://www.imdb.com" + value
        print(file)
        response = requests.get(file, stream=True)

        if response.ok:
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)

    with open(filename + "-fullcredits", 'wb') as handle:
        file = "http://www.imdb.com" + value + "fullcredits"
        print(file)
        response = requests.get(file, stream=True)

        if response.ok:
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
