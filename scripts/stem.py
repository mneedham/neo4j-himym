import nltk
import csv
from nltk.stem.lancaster import LancasterStemmer
from collections import defaultdict
from collections import Counter

episode_titles = {}
with open("data/import/episodes_full.csv", "r") as file:
    reader = csv.reader(file, delimiter = ",")
    reader.next()
    for row in reader:
        episode_titles[int(row[0])] = row[6]

episodes = defaultdict(str)
with open("data/import/sentences.csv", "r") as file:
    reader = csv.reader(file, delimiter=",")
    reader.next()

    for row in reader:
        episodes[int(row[1])] += row[4] + " "

st = LancasterStemmer()

stems_to_find = ["slap"]
words_to_find = ["bet"]

for episode, text in  episodes.iteritems():
    c = Counter()
    for sent in nltk.sent_tokenize(text.decode("utf-8")):
        # c = Counter()
        for word in nltk.word_tokenize(sent):
            stem = st.stem(word)
            if any(stem == stem_to_find for stem_to_find in stems_to_find) or \
               any(word == word_to_find for word_to_find in words_to_find):
                c[stem] += 1
        # if len(c.items()) == len(stems_to_find + words_to_find):
        #     print episode, episode_titles[episode],  c
    words_found = [x[0] for x in c.most_common()]
    if len(c.items()) == len(stems_to_find + words_to_find):
        print episode, episode_titles[episode],  c
