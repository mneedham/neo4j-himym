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

# seasons, episode_ids = [], []
# with open("data/import/episodes.csv", "r") as episodesfile:
#     reader = csv.reader(episodesfile, delimiter = ",")
#     reader.next()
#     for row in reader:
#         seasons.append(int(row[3]))
#         episode_ids.append(int(row[0]))
#
# df = DataFrame.from_items([('Season', seasons), ('EpisodeId', episode_ids)])
# last_episode_in_season = list(df.groupby("Season").max()["EpisodeId"])

stoplist = stopwords.words('english')
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
for id, episode in sorted(episodes.iteritems(), key=lambda t: int(t[0])):
    texts.append([item for sublist in episode for item in sublist])

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once and
                                not all([c in string.punctuation for c in word]) and
                                len(word) > 1]
          for text in texts]

dictionary = corpora.Dictionary(texts)
# dictionary.save('/tmp/himym.dict')

corpus = [dictionary.doc2bow(text) for text in texts]
# corpora.MmCorpus.serialize('/tmp/himym.mm', corpus)

# Find the most popular words over the first season
c = Counter()
for episode in corpus:
    for k,v in episode:
        c[k] += v

for word_id, count in c.most_common(10):
    print '{0: <5}'.format(count), dictionary[word_id]

# dictionary = corpora.Dictionary.load('/tmp/himym.dict')
# corpus = corpora.MmCorpus('/tmp/himym.mm')

tfidf = models.TfidfModel(corpus)
corpus_tfidf = tfidf[corpus]

words_tfidf = defaultdict(list)
count = 0
for doc in corpus_tfidf:
    for word_id,score in doc:
        words_tfidf[count].append((dictionary.id2token[word_id], score))
    count = count + 1


with open("data/import/words_tfidf.csv", "w") as wordsfile:
    writer = csv.writer(wordsfile, delimiter=",")
    writer.writerow(["EpisodeId", "Word", "Score"])

    for doc in words_tfidf:
        for word,score in sorted(words_tfidf[doc], key=lambda item: item[1] *-1):
            writer.writerow([doc+1, word.encode('utf8'), score])
    # print sorted(words_tfidf[doc], key=lambda item: item[1] *-1)[:5]

# for doc in words_tfidf:
#     print words_tfidf[doc]

# max(words_tfidf[0], key=lambda item:item[1])
# sorted(words_tfidf[0], key=lambda item: item[1] *-1)[:5]
#
# lsi = models.LsiModel(corpus_tfidf, id2word=dictionary, num_topics=2) # initialize an LSI transformation
# corpus_lsi = lsi[corpus_tfidf] # create a double wrapper over the original corpus: bow->tfidf->fold-in-lsi
#
# # what score does a documentation have with each topic
# for doc in corpus_lsi:
#     print(doc)
#
# lsi.save('/tmp/model.lsi') # same for tfidf, lda, ...
# lsi = models.LsiModel.load('/tmp/model.lsi')
#
# hdp = models.hdpmodel.HdpModel(corpus, id2word=dictionary)
#
# for doc in hdp[corpus_tfidf]:
#     print doc
#
# for topic in hdp.show_topics():
#     print topic
#
# dictionary = corpora.Dictionary.load('/tmp/himym.dict')
#
# lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
# doc = "Human computer interaction"
# vec_bow = dictionary.doc2bow(doc.lower().split())
# vec_lsi = lsi[vec_bow] # convert the query to LSI space
# print(vec_lsi)
#
# index = similarities.MatrixSimilarity(lsi[corpus])
# index.save('/tmp/himym.index')
# sims = index[vec_lsi] # perform a similarity query against the corpus
#
# print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples
#
# sims = sorted(enumerate(sims), key=lambda item: -1 * item[1])
#
# print sims
