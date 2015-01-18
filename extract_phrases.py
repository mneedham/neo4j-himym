import nltk
import csv
import string
from collections import Counter
import re

non_speaker = re.compile('[A-Za-z]+: (.*)')

def untokenize(ngram):
    tokens = list(ngram)
    return "".join([" "+i if not i.startswith("'") and \
                             i not in string.punctuation and \
                             i != "n't"
                          else i for i in tokens]).strip()

def extract_phrases(text, phrase_counter, length):
    for sent in nltk.sent_tokenize(text):
        strip_speaker = non_speaker.match(sent)
        if strip_speaker is not None:
            sent = strip_speaker.group(1)
        words = nltk.word_tokenize(sent)
        for phrase in nltk.util.ngrams(words, length):
            if all(word not in string.punctuation for word in phrase):
                phrase_counter[untokenize(phrase)] += 1

phrase_counter = Counter()

with open("data/import/sentences.csv", "r") as sentencesfile:
    reader = csv.reader(sentencesfile, delimiter=",")
    reader.next()
    count = 0
    for sentence in reader:
        extract_phrases(sentence[4], phrase_counter, 3)
        count = count + 1
        # if count > 1000:
        #     break

most_common_phrases = phrase_counter.most_common(500)
for k,v in most_common_phrases:
    print '{0: <5}'.format(v), k
