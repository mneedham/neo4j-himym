import csv
import requests
from bs4 import BeautifulSoup
from soupselect import select

import time
import datetime

episode_guide = open("data/Episode_Guide", 'r')

soup = BeautifulSoup(episode_guide.read())

with open('data/episodes.csv', 'w') as episodes:
    writer = csv.writer(episodes, delimiter=',')
    writer.writerow(["NumberOverall", "NumberInSeason", "Episode", "Season", "DateAired", "Timestamp"])

    for row in select(soup, 'tr'):
        link_to_episode = select(row.contents[3], "a")
        if len(link_to_episode) > 0:
            number_overall = row.contents[1].text.strip()
            number_in_season = row.contents[2].text.strip()
            episode = link_to_episode[0].get("href").replace('"', '').strip()

            date_aired = row.contents[4].text.strip()
            timestamp = int(time.mktime(datetime.datetime.strptime(date_aired, "%B %d, %Y").timetuple()))

            if number_overall == "216":
                number_overall = "180"
                number_in_season = "20"

            if int(number_overall) < 23:
                season = 1
            elif int(number_overall) < 45:
                season = 2
            elif int(number_overall) < 65:
                season = 3
            elif int(number_overall) < 89:
                season = 4
            elif int(number_overall) < 113:
                season = 5
            elif int(number_overall) < 137:
                season = 6
            elif int(number_overall) < 161:
                season = 7
            elif int(number_overall) < 185:
                season = 8
            else:
                season = 9

            writer.writerow([number_overall, number_in_season, episode, season, date_aired, timestamp])
