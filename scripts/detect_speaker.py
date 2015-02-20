import nltk
import json
import pickle

from sklearn.cross_validation import train_test_split
from himymutil.ml import pos_features

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

classifier = nltk.NaiveBayesClassifier.train(train_data)
print nltk.classify.accuracy(classifier, test_data)

with open("classifiers/bayes.pickle", "w") as f:
    pickle.dump(classifier, f)

classifier = nltk.DecisionTreeClassifier.train(train_data)
print nltk.classify.accuracy(classifier, test_data)

with open("classifiers/decision_tree.pickle", "w") as f:
    pickle.dump(classifier, f)

sentence = "Ted from 2030: Oh,we were bigfansofNewYork'sannualHalloweenparade.Idon'tmeantheonethattakesplaceHalloweennightintheVillage.ImeantheonethattakesplacethemorningofNovember1st,theAnnualPostHalloweenWalkofShameParade."
tokenized_sentence = nltk.word_tokenize(sentence)
for i, word in enumerate(tokenized_sentence):
    print "{0} -> {1}".format(word, classifier.classify(pos_features(tokenized_sentence, i)))
