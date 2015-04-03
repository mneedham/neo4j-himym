import csv
import nltk
import string
from nltk.collocations import *

# http://stackoverflow.com/questions/2452982/how-to-extract-common-significant-phrases-from-a-series-of-text-entries
# http://en.wikipedia.org/wiki/Mutual_information
# http://www.nltk.org/howto/collocations.html

sentences = []
with open("data/import/sentences.csv", "r") as sentencesfile:
    reader = csv.reader(sentencesfile, delimiter = ",")
    reader.next()
    for row in reader:
        sentence = [word
                    for word in nltk.word_tokenize(row[4].decode("utf-8").lower())
                    if word not in string.punctuation]
        sentences.append(sentence)


bigram_measures = nltk.collocations.BigramAssocMeasures()
trigram_measures = nltk.collocations.TrigramAssocMeasures()

# change this to read in your data
flattened_sentence = [word for sentence in sentences for word in sentence]
finder = BigramCollocationFinder.from_words(flattened_sentence)

# only bigrams that appear 3+ times
finder.apply_freq_filter(3)

# return the 10 n-grams with the highest PMI
for phrase in finder.nbest(bigram_measures.pmi, 50):
    print phrase

# most freq
for phrase, score in sorted(finder.ngram_fd.items(), key=lambda t: (-t[1], t[0]))[:50]:
    print phrase, score
