import nltk
import csv
import string
from gensim.models import Phrases
from gensim.models import Word2Vec
from nltk.corpus import stopwords

sentences = []
bigram = Phrases()
with open("data/import/sentences.csv", "r") as sentencesfile:
    reader = csv.reader(sentencesfile, delimiter = ",")
    reader.next()
    for row in reader:
        sentence = [word.decode("utf-8")
                    for word in nltk.word_tokenize(row[4].lower())
                    if word not in string.punctuation]
        sentences.append(sentence)
        bigram.add_vocab([sentence])

bigram_counter = Counter()
for key in bigram[sentences].vocab.keys():
    if key not in stopwords.words("english"):
        if len(key.split("_")) > 1:
            bigram_counter[key] += bigram.vocab[key]

for key, counts in bigram_counter.most_common(50):
    print '{0: <20} {1}'.format(key.encode("utf-8"), counts)

bigram_model = Word2Vec(bigram[sentences], size=100)
bigram_model_counter = Counter()
for key in bigram_model.vocab.keys():
    if key not in stopwords.words("english"):
        if len(key.split("_")) > 1:
            bigram_model_counter[key] += bigram_model.vocab[key].count

for key, counts in bigram_model_counter.most_common(50):
    print '{0: <20} {1}'.format(key.encode("utf-8"), counts)


trigram = Phrases(bigram[sentences])
trigram_model = Word2Vec(trigram[sentences], size=100)

c = Counter()
for key in trigram_model.vocab.keys():
    if key not in stopwords.words("english"):
        if len(key.split("_")) > 2:
            c[key] += trigram_model.vocab[key].count

for key, counts in c.most_common():
    print '{0: <20} {1}'.format(key.encode("utf-8"), counts)

# model.most_similar(['marshall', 'lily'], ['ted'], topn=3)
# bigram.vocab.viewkeys()
# bigram[nltk.word_tokenize("suit up")]
