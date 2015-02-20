import csv
import string
import nltk
import matplotlib
matplotlib.use('TkAgg')
import pylab
import matplotlib.pyplot as plt
pylab.show()
import pandas

from collections import defaultdict
from gensim import corpora
from pandas import DataFrame


last_episode_in_season = list(df.groupby("Season").max()["NumberOverall"])

episodes = defaultdict(list)
with open("data/import/sentences.csv", "r") as sentencesfile:
    reader = csv.reader(sentencesfile, delimiter = ",")
    reader.next()
    for row in reader:
        episodes[row[1]].append([ word for word in nltk.word_tokenize(row[4].lower())] )

texts = []
for id, episode in episodes.iteritems():
    texts.append([item for sublist in episode for item in sublist])

dictionary = corpora.Dictionary(texts)
corpus = [dictionary.doc2bow(text) for text in texts]

print "generate plot"

words = ["ted", "robin", "barney", "lily", "marshall"]
words_dict = dict()
for word in words:
    word_id = dictionary.token2id[word]
    counts = []
    for episode in corpus:
        count = dict(episode).get(word_id) or 0
        counts.append(count)
    words_dict[word] = counts

for word, counts in words_dict.iteritems():
    print word, counts[:5]

y_max = max([max(count) for count in words_dict.values()])

for word, counts in words_dict.iteritems():
    plt.figure()
    plt.plot(counts)
    for episode in last_episode_in_season:
        plt.axvline(x=episode, color = "red")
    plt.legend([word], loc='upper left')
    plt.ylabel('occurrences')
    plt.xlabel('episode')
    plt.xlim(0, 208)
    plt.ylim(0, y_max)
    plt.savefig('images/%s.pdf' % (word), dpi=100)

for word, counts in words_dict.iteritems():
    plt.figure()
    plt.plot(counts)
    for episode in last_episode_in_season:
        plt.axvline(x=episode, color = "red")
    plt.legend([word], loc='upper left')
    plt.ylabel('occurrences')
    plt.xlabel('episode')
    plt.xlim(0, 208)
    plt.ylim(0, y_max)
    plt.savefig('images/%s.png' % (word), dpi=200)
