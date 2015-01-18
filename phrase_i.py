import nltk
import csv
import string
from collections import Counter
import re

class PhraseCounter:
    """Keep count of phrases in a corpus"""
    def __init__(self):
        self.counter = Counter()
        self.non_speaker = re.compile('[A-Za-z]+: (.*)')

    def untokenize(self, ngram):
        tokens = list(ngram)
        return "".join([" "+i if not i.startswith("'") and \
                                 i not in string.punctuation and \
                                 i != "n't"
                              else i for i in tokens]).strip()

    def extract_phrases(self, text, length):
        for sent in nltk.sent_tokenize(text):
            strip_speaker = self.non_speaker.match(sent)
            if strip_speaker is not None:
                sent = strip_speaker.group(1)
            words = nltk.word_tokenize(sent)
            for phrase in nltk.util.ngrams(words, length):
                if all(word not in string.punctuation for word in phrase):
                    if phrase[0] == "I":
                        self.counter[self.untokenize(phrase)] += 1

    def most_common(self, count = None):
        if count is None:
            return self.counter.most_common()
        else:
            return self.counter.most_common(count)

if __name__ == "__main__":
    phrase_counter = PhraseCounter()

    with open("data/import/sentences.csv", "r") as sentencesfile:
        reader = csv.reader(sentencesfile, delimiter=",")
        reader.next()
        count = 0
        for sentence in reader:
            # if count > 5000:
            #     break
            phrase_counter.extract_phrases(sentence[4], 3)
            count = count + 1

    most_common_phrases = phrase_counter.most_common(500)
    for phrase,count in most_common_phrases:
        print '{0: <5}'.format(count), phrase
