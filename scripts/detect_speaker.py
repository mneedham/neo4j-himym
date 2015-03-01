import nltk
import json
import collections
import copy

from sklearn.cross_validation import train_test_split
from tabulate import tabulate
from himymutil.naive import NaiveClassifier
from himymutil.ml import pos_features, assess_classifier

with open("data/import/trained_sentences.json", "r") as json_file:
    json_data = json.load(json_file)

tagged_sents = []
for sentence in json_data:
    tagged_sents.append([(word["word"], word["speaker"]) for word in sentence["words"]])

featuresets = []
for tagged_sent in tagged_sents:
    untagged_sent = nltk.tag.untag(tagged_sent)
    sentence_pos = nltk.pos_tag(untagged_sent)
    for i, (word, tag) in enumerate(tagged_sent):
        featuresets.append((pos_features(untagged_sent, sentence_pos, i), tag) )

train_data,test_data = train_test_split(featuresets, test_size=0.20, train_size=0.80)

table = []
table.append(assess_classifier(NaiveClassifier(), test_data, "Naive"))
table.append(assess_classifier(nltk.NaiveBayesClassifier.train(train_data), test_data, "Naive Bayes"))
table.append(assess_classifier(nltk.DecisionTreeClassifier.train(train_data), test_data, "Decision Tree All In"))

def get_rid_of(entry, *keys):
    for key in keys:
        del entry[key]

tmp_train_data = copy.deepcopy(train_data)
for entry, tag in tmp_train_data:
    get_rid_of(entry, 'prev-word-pos', 'word-pos', 'next-word-pos')

tmp_test_data = copy.deepcopy(test_data)
for entry, tag in tmp_test_data:
    get_rid_of(entry, 'prev-word-pos', 'word-pos', 'next-word-pos')

table.append(assess_classifier(nltk.DecisionTreeClassifier.train(tmp_train_data), tmp_test_data, "Decision Tree Words"))

tmp_train_data = copy.deepcopy(train_data)
for entry, tag in tmp_train_data:
    get_rid_of(entry, 'prev-word', 'word', 'next-word')

tmp_test_data = copy.deepcopy(test_data)
for entry, tag in tmp_test_data:
    get_rid_of(entry, 'prev-word', 'word', 'next-word')

table.append(assess_classifier(nltk.DecisionTreeClassifier.train(tmp_train_data), tmp_test_data, "Decision Tree POS"))

print(tabulate(table, headers=["Classifier","speaker precision", "speaker recall", "non-speaker precision", "non-speaker recall"]))
