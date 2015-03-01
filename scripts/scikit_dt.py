import json
import nltk

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

#train_data,test_data = train_test_split(featuresets, test_size=0.20, train_size=0.80)

X = vec.fit_transform([item[0] for item in train_data]).toarray()
Y = [item[1] for item in train_data]
X_train, X_test,Y_train, Y_test = train_test_split(X, Y, test_size=0.20, train_size=0.80)

clf = clf.fit(X_train, Y_train)
predictions = clf.predict(X_test)

predictions_actual = zip(predictions, Y_test)

refsets = collections.defaultdict(set)
testsets = collections.defaultdict(set)

for i, (prediction, actual) in enumerate(predictions_actual):
    refsets[actual].add(i)
    testsets[prediction].add(i)

speaker_precision = nltk.metrics.precision(refsets[True], testsets[True])
speaker_recall = nltk.metrics.recall(refsets[True], testsets[True])
non_speaker_precision = nltk.metrics.precision(refsets[False], testsets[False])
non_speaker_recall = nltk.metrics.recall(refsets[False], testsets[False])
print [speaker_precision, speaker_recall, non_speaker_precision, non_speaker_recall]
