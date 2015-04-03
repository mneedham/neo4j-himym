import csv
import operator
import nltk
import string
from collections import defaultdict, Counter
from nltk.util import ngrams
from nltk.corpus import stopwords

stop_words = list(string.punctuation) + stopwords.words('english') + ["ted", "barney", "marshall", "lily", "robin", "gon", "na", "wanna", "flashback"]

episodes = defaultdict(str)
with open("data/import/sentences.csv", "r") as file:
    reader = csv.reader(file, delimiter = ",")
    reader.next()
    for row in reader:
        episodes[row[1]] += row[4] + " "

def default_dict_function():
   return {"total": 0, "episodes": set()}

tokens = defaultdict(default_dict_function)

for episode_id, text in episodes.iteritems():
    text = text.lower().decode("utf-8")
    for sent in nltk.sent_tokenize(text):
        words = [word for word in nltk.word_tokenize(sent) if word not in stop_words]
        values = ["_".join(value) for value in list(ngrams(words,3))]
        for word in values:
            tokens[word]["total"] += 1
            tokens[word]["episodes"].add(episode_id)

import math
import numpy as np
import matplotlib
matplotlib.use('TkAgg')
import matplotlib.pyplot as plt

values = range(1, 209)
probs = [1.0 / 208] * 208

for idx, prob in enumerate(probs):
    if idx > 3 and idx < 10:
        probs[idx] = probs[idx] * (1 + math.log(idx + 1))
    if idx > 10 and idx < 20:
        probs[idx] = probs[idx] * (1 + math.log((40 - idx) + 1))

probs = [p / sum(probs) for p in probs]
sample =  np.random.choice(values, 1000, p=probs)

# print sorted(tokens.items(), key = lambda x: x[1]["total"] *-1)[:10]
# print sorted(tokens.items(), key = lambda x: len(x[1]["episodes"]) *-1)[:10]

for term, item in tokens.iteritems():
    num_episodes = len(item["episodes"])
    num_occurrences = item["total"]
    bin_score = np.bincount(sample)[num_episodes]
    score = math.log(num_occurrences) *  (bin_score * 1.0 / len(sample))
    tokens[term]["score"] = score

for term, item in sorted(tokens.items(), key = lambda x: x[1]["score"] *-1)[:50]:
    num_episodes = len(item["episodes"])
    num_occurrences = item["total"]
    bin_score = np.bincount(sample)[num_episodes]
    score = math.log(num_occurrences) *  (bin_score * 1.0 / len(sample))

    print "{0: <20} {1: <5} {2: <5} {3: <3} {4: <10}".format(term.encode("utf-8"), num_occurrences, num_episodes, bin_score, item["score"])
