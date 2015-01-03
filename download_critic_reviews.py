import requests
from bs4 import BeautifulSoup
from soupselect import select

episodes = {}
for i in range(1,10):
    page = open("data/tv-critic/season-" + str(i), 'r')
    soup = BeautifulSoup(page.read())

    for row in select(soup, "div.typography tr"):
        columns = select(row, "td")
        if len(columns) > 0:
            episodes["%d-%d" %(i, int(columns[0].text))] = int(columns[3].text)

print episodes

# for key, value in episodes.iteritems():
#     parts = key.split("x")
#     season = int(parts[0])
#     episode = int(parts[1])
#     filename = "data/transcripts/S%d-Ep%d" %(season, episode)
#     print filename
#
#     with open(filename, 'wb') as handle:
#         headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_9_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
#         response = requests.get("http://transcripts.foreverdreaming.org" + value["link"], headers = headers)
#         if response.ok:
#             for block in response.iter_content(1024):
#                 if not block:
#                     break
#
#                 handle.write(block)
