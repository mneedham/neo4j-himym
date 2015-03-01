import nltk
import collections

def pos_features(sentence, sentence_pos, i):
    features = {}

    features["word"] = sentence[i]
    features["word-pos"] = sentence_pos[i][1]

    if i == 0:
        features["prev-word"] = "<START>"
        features["prev-word-pos"] = "<START>"
    else:
        features["prev-word"] = sentence[i-1]
        features["prev-word-pos"] = sentence_pos[i-1][1]

    if i == len(sentence) - 1:
        features["next-word"] = "<END>"
        features["next-word-pos"] = "<END>"
    else:
        features["next-word"] = sentence[i+1]
        features["next-word-pos"] = sentence_pos[i+1][1]

    return features

def assess_classifier(classifier, test_data, text):
    refsets = collections.defaultdict(set)
    testsets = collections.defaultdict(set)
    for i, (feats, label) in enumerate(test_data):
        refsets[label].add(i)
        observed = classifier.classify(feats)
        testsets[observed].add(i)
    speaker_precision = nltk.metrics.precision(refsets[True], testsets[True])
    speaker_recall = nltk.metrics.recall(refsets[True], testsets[True])
    non_speaker_precision = nltk.metrics.precision(refsets[False], testsets[False])
    non_speaker_recall = nltk.metrics.recall(refsets[False], testsets[False])
    return [text, speaker_precision, speaker_recall, non_speaker_precision, non_speaker_recall]
