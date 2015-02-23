import nltk
import json
import pickle
import collections

from sklearn.cross_validation import train_test_split
from himymutil.ml import pos_features
from himymutil.naive import NaiveClassifier
from tabulate import tabulate

with open("data/import/trained_sentences.json", "r") as json_file:
    json_data = json.load(json_file)

tagged_sents = []
for sentence in json_data:
    tagged_sents.append([(word["word"], word["speaker"]) for word in sentence["words"]])

featuresets = []
for tagged_sent in tagged_sents:
    untagged_sent = nltk.tag.untag(tagged_sent)
    for i, (word, tag) in enumerate(tagged_sent):
        featuresets.append( (pos_features(untagged_sent, i), tag) )

train_data,test_data = train_test_split(featuresets, test_size=0.20, train_size=0.80)

def assess_classifier(classifier, test_data, text):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(test_data):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)

    speaker_precision = nltk.metrics.precision(refsets[True], testsets[True])
    speaker_recall = nltk.metrics.recall(refsets[True], testsets[True])
    speaker_f_measure = nltk.metrics.f_measure(refsets[True], testsets[True])

    non_speaker_precision = nltk.metrics.precision(refsets[False], testsets[False])
    non_speaker_recall = nltk.metrics.recall(refsets[False], testsets[False])
    non_speaker_f_measure = nltk.metrics.f_measure(refsets[False], testsets[False])

    table = [["speaker precision", speaker_precision],
             ["speaker recall", speaker_recall],
             ["speaker F-measure", speaker_f_measure],
             ["non-speaker precision", non_speaker_precision],
             ["non-speaker recall", non_speaker_recall],
             ["non-speaker F-measure", non_speaker_f_measure]]

    print(tabulate(table, headers=["Measure","Naive Bayes"]))

    with open("classifiers/" + text.lower().replace(" ", "_") + ".pickle", "w") as f:
        pickle.dump(classifier, f)

assess_classifier(nltk.NaiveBayesClassifier.train(train_data), test_data, "Naive Bayes")
# assess_classifier(nltk.DecisionTreeClassifier.train(train_data), test_data, "Decision Tree")
# assess_classifier(NaiveClassifier(), test_data, "Naive")

# sentence = "Ted from 2030: Oh,we were"
# tokenized_sentence = nltk.word_tokenize(sentence)
# for i, word in enumerate(tokenized_sentence):
#     print "{0} -> {1}".format(word, classifier.classify(pos_features(tokenized_sentence, i)))
