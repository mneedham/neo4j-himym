import logging
import csv
import string
import nltk
from gensim import corpora, models, similarities
from nltk.corpus import stopwords
from collections import defaultdict, Counter
import matplotlib
matplotlib.use('TkAgg')
import pylab
import matplotlib.pyplot as plt
pylab.show()

import pandas
from pandas import DataFrame

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

stoplist = stopwords.words('english')

seasons, episode_ids = [], []
with open("data/import/episodes.csv", "r") as episodesfile:
    reader = csv.reader(episodesfile, delimiter = ",")
    reader.next()
    for row in reader:
        seasons.append(int(row[3]))
        episode_ids.append(int(row[0]))

df = DataFrame.from_items([('Season', seasons), ('EpisodeId', episode_ids)])
last_episode_in_season = list(df.groupby("Season").max()["EpisodeId"])

print "process sentences"

episodes = defaultdict(list)
with open("data/import/sentences.csv", "r") as sentencesfile:
    reader = csv.reader(sentencesfile, delimiter = ",")
    reader.next()
    for row in reader:
        episodes[row[1]].append([ word
                                    for word in nltk.word_tokenize(row[4].lower())
                                    if word not in string.punctuation and
                                       word not in stoplist ] )

texts = []
for id, episode in episodes.iteritems():
    texts.append([item for sublist in episode for item in sublist])

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
          for text in texts]

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

print "generate plot"

words = ["ted", "robin", "barney", "lily", "marshall"]
for word in words:
    plt.figure()
    word_id = dictionary.token2id[word]
    counts = []
    for episode in corpus:
        count = dict(episode).get(word_id) or 0
        counts.append(count)
    plt.plot(counts)
    for episode in last_episode_in_season:
        plt.axvline(x=episode, color = "red")
    plt.legend([word], loc='upper left')
    plt.ylabel('occurrences')
    plt.xlabel('episode')
    # plt.show()
    print "save plot"
    plt.savefig('images/%s.pdf' % (word), dpi=100)
