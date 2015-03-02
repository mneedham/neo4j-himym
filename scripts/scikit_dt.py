import json
import nltk
import collections

from tabulate import tabulate
from himymutil.ml import pos_features, assess_classifier
from sklearn import tree
from sklearn.cross_validation import train_test_split
from sklearn.feature_extraction import DictVectorizer

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

vec = DictVectorizer()
X = vec.fit_transform([item[0] for item in featuresets]).toarray()
Y = [item[1] for item in featuresets]
X_train, X_test,Y_train, Y_test = train_test_split(X, Y, test_size=0.20, train_size=0.80)

def assess(text, predictions_actual):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (prediction, actual) in enumerate(predictions_actual):
        refsets[actual].add(i)
        testsets[prediction].add(i)
    speaker_precision = nltk.metrics.precision(refsets[True], testsets[True])
    speaker_recall = nltk.metrics.recall(refsets[True], testsets[True])
    non_speaker_precision = nltk.metrics.precision(refsets[False], testsets[False])
    non_speaker_recall = nltk.metrics.recall(refsets[False], testsets[False])
    return [text, speaker_precision, speaker_recall, non_speaker_precision, non_speaker_recall]

table = []

clf = tree.DecisionTreeClassifier()
clf = clf.fit(X_train, Y_train)
predictions = clf.predict(X_test)
assessment = assess("Decision Tree", zip(predictions, Y_test))

table.append(assessment)

# table.append(["Decision Tree", speaker_precision, speaker_recall, non_speaker_precision, non_speaker_recall])

print(tabulate(table, headers=["Classifier","speaker precision", "speaker recall", "non-speaker precision", "non-speaker recall"]))

with open("/tmp/decisionTree.dot", 'w') as file:
    tree.export_graphviz(clf, out_file = file, feature_names = vec.get_feature_names())

# dot -Tpng /tmp/decisionTree.dot -o /tmp/decisionTree.png
