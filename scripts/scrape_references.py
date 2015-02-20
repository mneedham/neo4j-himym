import requests
from bs4 import BeautifulSoup
from soupselect import select
import csv

episode_dict = {}
with open("data/import/episodes_full.csv") as episodes:
    reader = csv.reader(episodes, delimiter=',')
    reader.next()

    for row in reader:
        episode_dict[row[6].lower()] = {
            "id": int(row[0]),
            "title": row[6],
            "file": row[2],
            "season": row[3],
            "number": row[1]
        }

with open("data/import/references.csv", "w") as references:
    writer = csv.writer(references, delimiter=",")
    writer.writerow(["ReferencedEpisodeId", "ReferencingEpisodeId", "ReferenceText"])

    for key, value in episode_dict.iteritems():
        filename = "data" + value["file"]
        soup = BeautifulSoup(open(filename, "r").read())
        print "Season %s Episode %s" %(value["season"], value["number"])
        future_references_header = select(soup, 'span#Future_References_.28Contains_Spoilers.29')

        if len(future_references_header) > 0:
            references = select(future_references_header[0].find_parent("h2").next_sibling.next_sibling, "li")

            for reference in references:
                links = select(reference, "a")
                for link in links:
                    episode = episode_dict.get(link.text.lower())
                    if episode:
                        writer.writerow([value["id"], episode["id"], reference.text.strip().encode("utf-8")])
