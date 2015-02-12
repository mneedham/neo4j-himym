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

bigram.vocab.viewkeys()
bigram[nltk.word_tokenize("suit up")]

model = Word2Vec(bigram[sentences], size=100)
model.save("phrases")

model.most_similar(['marshall', 'lily'], ['ted'], topn=3)

c = Counter()
for key in model.vocab.keys():
    if key not in stopwords.words("english"):
        if len(key.split("_")) > 1:
            c[key] += model.vocab[key].count

for key, counts in c.most_common():
    print '{0: <20} {1}'.format(key.encode("utf-8"), counts)

# for word in model.vocab:
#     print word
