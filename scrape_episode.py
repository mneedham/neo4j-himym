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

episode_rankings = {}
for i in range(1,10):
    page = open("data/tv-critic/season-" + str(i), 'r')
    soup = BeautifulSoup(page.read())

    for row in select(soup, "div.typography tr"):
        columns = select(row, "td")
        if len(columns) > 0:
            episode_rankings["%d-%d" %(i, int(columns[0].text))] = int(columns[3].text)

print episode_rankings

with open('data/import/episodes.csv', 'r') as episodes:
    reader = csv.reader(episodes, delimiter=',')
    reader.next()

    with open('data/import/episodes_full.csv', 'w') as fullepisodes:
        writer = csv.writer(fullepisodes, delimiter=',')
        writer.writerow(["NumberOverall", "NumberInSeason", "Episode", "Season", "DateAired", "Timestamp", "Title", "Director", "Viewers", "Writers", "Rating"])

        for row in reader:
            row.append(episode_dict[row[0]]['title'].encode('utf-8'))
            row.append(episode_dict[row[0]]['director'].encode('utf-8'))
            row.append(episode_dict[row[0]]['viewers'].encode('utf-8'))
            row.append(",".join(episode_dict[row[0]]['writers']))

            ranking = episode_rankings.get("%s-%s" %(row[3], row[1]))
            row.append(ranking)

            writer.writerow(row)
