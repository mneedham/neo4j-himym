import requests
from bs4 import BeautifulSoup
from soupselect import select
import csv

episodes = open("data/List_of_How_I_Met_Your_Mother_episodes", 'r').read()
soup = BeautifulSoup(episodes)
rows = select(soup, 'tr.vevent')

episode_dict = {}

for row in rows:
    columns = select(row, "td")
    episode_dict[select(row, "th")[0].text] = {
        "season_id": columns[0].text,
        "title": select(columns[1], "a")[0].text,
        "director": columns[2].text,
        "writers": [writer.strip() for writer in columns[3].text.split("&")],
        "viewers": columns[6].contents[0]
    }

print episode_dict

with open('data/episodes.csv', 'r') as episodes:
    reader = csv.reader(episodes, delimiter=',')
    reader.next()

    with open('data/episodes_full.csv', 'w') as fullepisodes:
        writer = csv.writer(fullepisodes, delimiter=',')
        writer.writerow(["NumberOverall", "NumberInSeason", "Episode", "Season", "DateAired", "Timestamp", "Title", "Director", "Viewers", "Writers"])

        for row in reader:
            row.append(episode_dict[row[0]]['title'].encode('utf-8'))
            row.append(episode_dict[row[0]]['director'].encode('utf-8'))
            row.append(episode_dict[row[0]]['viewers'].encode('utf-8'))
            row.append(",".join(episode_dict[row[0]]['writers']))
            writer.writerow(row)
