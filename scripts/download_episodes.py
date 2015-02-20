import requests
from bs4 import BeautifulSoup
from soupselect import select

episode_guide = open("data/Episode_Guide", 'r')

soup = BeautifulSoup(episode_guide.read())

pages = []

for row in select(soup, 'td a'):
    pages.append(row.get("href"))

for page in pages:
    with open("data/" + page[1:], 'wb') as handle:
        file = "http://how-i-met-your-mother.wikia.com" + page
        print(file)
        response = requests.get(file, stream=True)

        if response.ok:
            # Something went wrong

            for block in response.iter_content(1024):
                if not block:
                    break

                handle.write(block)
