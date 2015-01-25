import logging
import csv

from gensim import corpora, models, similarities
from nltk.corpus import stopwords

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

episodes = dict()
for i in range(1, 23):
    episodes[str(i)] = []

with open("data/import/sentences.csv", "r") as sentencesfile:
    reader = csv.reader(sentencesfile, delimiter = ",")
    reader.next()
    for row in reader:
        if row[2] == "1":
            episodes[row[3]].append(row[4])

for i in range(1,23):
    episodes[str(i)] = " ".join(episodes[str(i)])

documents = []
for id, episode in episodes.iteritems():
    documents.append(episode)

stoplist = stopwords.words('english')

documents = ["Human machine interface for lab abc computer applications",
              "A survey of user opinion of computer system response time",
              "The EPS user interface management system",
              "System and human system engineering testing of EPS",
              "Relation of user perceived response time to error measurement",
              "The generation of random binary unordered trees",
              "The intersection graph of paths in trees",
              "Graph minors IV Widths of trees and well quasi ordering",
              "Graph minors A survey"]

# remove common words and tokenize
stoplist = set('for a of the and to in'.split())
texts = [[word for word in document.lower().split() if word not in stoplist]
          for document in documents]

# remove words that appear only once
all_tokens = sum(texts, [])
tokens_once = set(word for word in set(all_tokens) if all_tokens.count(word) == 1)
texts = [[word for word in text if word not in tokens_once]
          for text in texts]

print(texts)

dictionary = corpora.Dictionary(texts)
dictionary.save('/tmp/deerwester.dict') # store the dictionary, for future reference
dictionary.save('/tmp/himym.dict')

print(dictionary.token2id)

new_doc = "Human computer interaction"
new_vec = dictionary.doc2bow(new_doc.lower().split())

corpus = [dictionary.doc2bow(text) for text in texts]
corpora.MmCorpus.serialize('/tmp/deerwester.mm', corpus) # store to disk, for later use
corpora.MmCorpus.serialize('/tmp/himym.mm', corpus)

dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')
corpus = corpora.MmCorpus('/tmp/deerwester.mm')

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

dictionary = corpora.Dictionary.load('/tmp/deerwester.dict')

lsi = models.LsiModel(corpus, id2word=dictionary, num_topics=2)
doc = "Human computer interaction"
vec_bow = dictionary.doc2bow(doc.lower().split())
vec_lsi = lsi[vec_bow] # convert the query to LSI space
print(vec_lsi)

index = similarities.MatrixSimilarity(lsi[corpus])
index.save('/tmp/deerwester.index')
sims = index[vec_lsi] # perform a similarity query against the corpus

print(list(enumerate(sims))) # print (document_number, document_similarity) 2-tuples

sims = sorted(enumerate(sims), key=lambda item: -1 * item[1])

print sims
