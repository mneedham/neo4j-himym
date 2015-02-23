import nltk
from nltk import ClassifierI

from himymutil.ml import pos_features

class NaiveClassifier(ClassifierI):
    def classify(self, featureset):
        if featureset['next-word'] == ":":
            return True
        else:
            return False

if __name__ == '__main__':
    classifier = NaiveClassifier()

    sentence = "Ted from 2030: Oh,we were bigfansofNewYork'sannualHalloweenparade.Idon'tmeantheonethattakesplaceHalloweennightintheVillage.ImeantheonethattakesplacethemorningofNovember1st,theAnnualPostHalloweenWalkofShameParade."
    tokenized_sentence = nltk.word_tokenize(sentence)
    for i, word in enumerate(tokenized_sentence):
        print "{0} -> {1}".format(word, classifier.classify(pos_features(tokenized_sentence, i)))
