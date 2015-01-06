import requests
import csv
import nltk
import re
import numpy as np
import nltk.data

from bs4 import BeautifulSoup
from soupselect import select
from nltk.corpus import stopwords
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize

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
        transcript = open("data/transcripts/S%s-Ep%s" %(row[3], row[1])).read()
        soup = BeautifulSoup(transcript)
        rows  = select(soup, "table.tablebg tr")

        text = rows[1].text.replace("How I Met Your Mother DVDs", "") \
            .replace("How I Met Your Mother Instant Video", "") \
            .replace("How I Met Your Mother Collectables", "") \
            .replace("Amazon Prime Instant Video Free Trial", "") \
            .replace("adsbygoogle", "") \
            .strip()

        text = re.sub("[^a-zA-Z]", " ", text )

        words =  nltk.word_tokenize(text)
        words = [w for w in words if not w in stopwords.words("english")]

        words = count_words(words)
        episodes_dict[row[0]] = words

with open("data/import/words.csv", "w") as words:
    writer = csv.writer(words, delimiter=",")
    writer.writerow(["EpisodeId", "Word", "Occurrences"])
    for episode_id, words in episodes_dict.iteritems():
        for word in words:
            writer.writerow([episode_id, word, words[word]])
