import csv
import nltk
import re

from bs4 import BeautifulSoup
from soupselect import select
from nltk.corpus import stopwords
from collections import Counter
from nltk.tokenize import word_tokenize

def count_words(words):
    tally=Counter()
    for elem in words:
        tally[elem] += 1
    return tally

episodes_dict = {}
with open('data/import/episodes.csv', 'r') as episodes:
    reader = csv.reader(episodes, delimiter=',')
    reader.next()

    for row in reader:
        print row
        transcript = open("data/transcripts/S%s-Ep%s" %(row[3], row[1])).read()
        soup = BeautifulSoup(transcript)
        rows = select(soup, "table.tablebg tr td.post-body div.postbody")

        raw_text = rows[0]
        [ad.extract() for ad in select(raw_text, "div.ads-topic")]
        [ad.extract() for ad in select(raw_text, "div.t-foot-links")]

        text = re.sub("[^a-zA-Z]", " ", raw_text.text.strip())
        words = [w for w in nltk.word_tokenize(text) if not w.lower() in stopwords.words("english")]

        episodes_dict[row[0]] = count_words(words)

with open("data/import/words.csv", "w") as words:
    writer = csv.writer(words, delimiter=",")
    writer.writerow(["EpisodeId", "Word", "Occurrences"])
    for episode_id, words in episodes_dict.iteritems():
        for word in words:
            writer.writerow([episode_id, word, words[word]])
