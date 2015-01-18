import nltk
import csv
import string
import re
import getopt
import sys

from nltk.collocations import *
from collections import Counter

non_speaker = re.compile('[A-Za-z]+: (.*)')

def check_for_phrase(row, phrase_counter, input_phrase):
    input_phrase = tuple(nltk.word_tokenize(input_phrase))
    for sent in nltk.sent_tokenize(row[4]):
        words = nltk.word_tokenize(sent)
        for phrase in nltk.util.ngrams(words, len(input_phrase)):
            if phrase == input_phrase:
                phrase_counter[int((row[2]))]["%s" % (row[3])] += 1

if __name__ == "__main__":
    phrase_to_lookup = sys.argv[1:][0]

    phrase_counter = dict()
    for season in range(1,10):
        phrase_counter[season] = Counter()

    with open("data/import/sentences.csv", "r") as sentencesfile:
        reader = csv.reader(sentencesfile, delimiter=",")
        reader.next()
        for sentence in reader:
            check_for_phrase(sentence, phrase_counter, phrase_to_lookup)

    for k,v in phrase_counter.iteritems():
        print k, v.most_common()
