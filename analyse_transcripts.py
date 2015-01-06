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
    tally

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

        # text =  "".join([str(x) for x in rows[1].contents])


        # print text.split("<br>\n<br>")
        text = re.sub("[^a-zA-Z]", " ", text )

        words =  nltk.word_tokenize(text)
        # print [word_tokenize(t) for t in sent_tokenize(text)]

        # punkt = nltk.data.load('tokenizers/punkt/english.pickle')
        # print punkt.tokenize(text)[2]

        words = [w for w in words if not w in stopwords.words("english")]

        words = set(words)
        words = set(nltk.ngrams(words, 2))
        episodes_dict[row[0]] = words


        # print nltk.ngrams(rows[1].text.strip(), 4)

tally=Counter()
for k,v in episodes_dict.iteritems():
    for v2 in v:
        tally[v2] +=1

print [(k, tally[k]) for k in tally if tally[k] > 1]
