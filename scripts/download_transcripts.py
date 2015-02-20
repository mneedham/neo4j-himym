import requests
from bs4 import BeautifulSoup
from soupselect import select

episodes = {}
for i in range(1,3):
    page = open("data/transcripts/page-" + str(i) + ".html", 'r')
    soup = BeautifulSoup(page.read())

    for row in select(soup, "td.topic-titles a"):
        parts = row.text.split(" - ")
        episodes[parts[0]] = {"title": parts[1], "link": row.get("href")}

for key, value in episodes.iteritems():
    parts = key.split("x")
    season = int(parts[0])
    episode = int(parts[1])
    filename = "data/transcripts/S%d-Ep%d" %(season, episode)
    print filename

    with open(filename, 'wb') as handle:
        headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
        response = requests.get("http://transcripts.foreverdreaming.org" + value["link"], headers = headers)
        if response.ok:
            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
