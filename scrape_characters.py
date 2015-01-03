import requests
from bs4 import BeautifulSoup
from soupselect import select
import csv

with open('data/episodes.csv', 'r') as episodes:
    reader = csv.reader(episodes, delimiter=',')
    reader.next()

    with open('data/characters.csv', 'w') as characters:
        writer = csv.writer(characters, delimiter=',')
        writer.writerow(["EpisodeId", "Character", "Actor"])

        for row in reader:
            filename = "imdb/S%s-Ep%s-fullcredits" %(int(row[3]), int(row[1]))
            print filename
            characters_page = open(filename, 'r').read()
            soup = BeautifulSoup(characters_page)
            characters = select(soup, 'table.cast_list tr')

            for character_row in characters:
                columns = select(character_row, "td")
                if len(columns) > 1:
                    character = " ".join(select(character_row, "td.character")[0].text.replace("\n", "").split()).encode("utf-8")
                    actor = " ".join(select(character_row, "td.itemprop")[0].text.replace("\n", "").split()).encode("utf-8")

                    characters = character.split(" / ")

                    for c in characters:
                        c = c.replace("(credit only)", "").replace("(uncredited)","").strip()

                        writer.writerow([row[0], c, actor])
