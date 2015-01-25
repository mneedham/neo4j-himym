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
dictionary.save('/tmp/himym.dict')

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/himym.mm', corpus)

words = ["ted", "robin", "barney", "lily", "marshall"]
words = ["robin"]
for word in words:
    word_id = dictionary.token2id[word]
    counts = []
    for episode in corpus:
        count = dict(episode).get(word_id) or 0
        counts.append(count)
    print counts
    plt.plot(counts)

for episode in last_episode_in_season:
    plt.axvline(x=episode, color = "red")

plt.legend(words, loc='upper left')
plt.ylabel('occurrences')
plt.xlabel('episode')
plt.show()

# Find the most popular words over the first season
c = Counter()
for episode in corpus:
    for k,v in episode:
        c[k] += v

for word_id, count in c.most_common(10):
    print '{0: <5}'.format(count), dictionary[word_id]

dictionary = corpora.Dictionary.load('/tmp/himym.dict')
corpus = corpora.MmCorpus('/tmp/himym.mm')

tfidf = models.TfidfModel(corpus)

doc_bow = [(0, 1), (1, 1)]
tfidf[doc_bow]

corpus_tfidf = tfidf[corpus]
for doc in corpus_tfidf:
    print(doc)

lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi

# what score does a documentation have with each topic
for doc in corpus_lsi:
    print(doc)

lsi.save('/tmp/model.lsi') # same for tfidf, lda, ...
lsi = models.LsiModel.load('/tmp/model.lsi')

hdp = models.hdpmodel.HdpModel(corpus, id2word=dictionary)

for doc in hdp[corpus_tfidf]:
    print doc

for topic in hdp.show_topics():
    print topic

dictionary = corpora.Dictionary.load('/tmp/himym.dict')

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus])
index.save('/tmp/himym.index')
sims = index[vec_lsi] # perform a similarity query against the corpus

print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples

sims = sorted(enumerate(sims), key=lambda item: -1 * item[1])

print sims
