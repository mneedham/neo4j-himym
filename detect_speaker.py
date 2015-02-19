import nltk

def pos_features(sentence, i):
    features = {}
    features["word"] = sentence[i]
    if i == 0:
        features["prev-word"] = "<START>"
    else:
        features["prev-word"] = sentence[i-1]
    if i == len(sentence) - 1:
        features["next-word"] = "<END>"
    else:
        features["next-word"] = sentence[i+1]
    return features

tagged_sents = []
tagged_sents.append([('Narrator', 'Speaker'), (':', ''), ('Kids', ''), (',', ''), ('I', ''),("'m", ''), ('going', ''),
  ('to', ''), ('tell', ''), ('you', ''), ('an', ''), ('incredible', ''), ('story.', ''), ('The', ''), ('story', ''),
  ('of', ''), ('how', ''), ('I', ''), ('met', ''), ('your', ''), ('mother', '')])
tagged_sents.append([('Son', 'Speaker'), (':', ''), ('Are', ''), ('we', ''), ('being', ''), ('punished', ''), ('for', ''), ('something', ''), ('?', '')])
tagged_sents.append([('(', ''), ('Music', ''), ('Plays', ''), (',', ''), ('Title', ''), ('How', ''), ('I', ''), ('Met', ''), ('Your', ''), ('Mother', ''), ('appears', ''), (')', '')])
tagged_sents.append([('Daughter', 'Speaker'), (':', ''), ('Yeah', ''), (',', ''), ('is', ''), ('this', ''), ('going', ''), ('to', ''), ('take', ''), ('a', ''), ('while', ''), ('?', '')])
tagged_sents.append([('Narrator', 'Speaker'), (':', ''), ('No', '')])
tagged_sents.append([('(', ''), ('Scene', ''), ('Freezes', ''), (')', '')])
tagged_sents.append([('Barney', 'Speaker'), (':', ''), ('Where', ''), ("'s", ''), ('your', ''), ('suit', ''), ('!', ''), ('?', ''), ('Just', ''), ('once', ''), ('when', ''), ('I', ''), ('say', ''), ('suit', ''), ('up', ''), (',', ''), ('I', ''), ('wish', ''), ('you', ''), ("'d", ''), ('put', ''), ('on', ''), ('a', ''), ('suit', ''), ('.', '')])
tagged_sents.append([('Ted', 'Speaker'), ('(', 'Speaker'), ('2030', 'Speaker'), (')', 'Speaker'), (':', ''), ('The', ''), ('next', ''), ('night', ''), (',', ''), ('Barney', ''), ('and', ''), ('Nora', ''), ('saw', ''), ('each', ''), ('other', ''), ('for', ''), ('a', ''), ('coffee.Fortunately', ''), (',', ''), ('without', ''), ('the', ''), ('neck', ''), ('brace', ''), ('ridiculous', ''), ('.', '')])
tagged_sents.append([('Ted', 'Speaker'), ('(', 'Speaker'), ('2030', 'Speaker'), (')', 'Speaker'), (':', ''), ('But', ''), ('I', ''), ('lost', ''), ('a', ''), ('bit', ''), ('in', ''), ('the', ''), ('story', ''), ('.', '')])
tagged_sents.append([('(', ''), ('Barney', ''), ('hits', ''), ('Ted', ''), (')', '')])
tagged_sents.append([('[', ''), ('Fantasy', ''), ('Ends', ''), (']', '')])
tagged_sents.append([('Yasmine', 'Speaker'), (':', ''), ('So', ''), ('do', ''), ('you', ''), ('think', ''), ('you', ''), ("'ll", ''), ('ever', ''), ('get', ''), ('married', ''), ('?', '')])
tagged_sents.append([('Excuse', ''), ('me.', ''), ('It', ''), ('even', ''), ('has', ''), ('my', ''), ('initials', ''), ('on', ''), ('it', ''), ('right', ''), ('here', ''), (':', ''), ('T.M', ''), ('.', '')])
tagged_sents.append([('(', ''), ('sighs', ''), (')', ''), (':', ''), ('We', ''), ("'ll", ''), ('work', ''), ('on', ''), ('that', ''), ('.', '')])
tagged_sents.append([('Lily', 'Speaker'), (':', ''), ('(', ''), ('realizing', ''), (')', ''), ('No', ''), (',', ''), ('you', ''), ('are', ''), ('too', ''), ('old', ''), ('to', ''), ('be', ''), ('scared', ''), ('to', ''), ('open', ''), ('a', ''), ('bottle', ''), ('of', ''), ('champagne', ''), ('!', '')])
tagged_sents.append([('Marshall', 'Speaker'), (':', ''), ('Doggie', ''), ('style.', ''), ('(', ''), ('Laughs', ''), (')', '')])

featuresets = []
for tagged_sent in tagged_sents:
    untagged_sent = nltk.tag.untag(tagged_sent)
    for i, (word, tag) in enumerate(tagged_sent):
        featuresets.append( (pos_features(untagged_sent, i), tag) )

classifier = nltk.NaiveBayesClassifier.train(featuresets)
print(classifier.show_most_informative_features(5))
print nltk.classify.accuracy(classifier, featuresets)

classifier = nltk.DecisionTreeClassifier.train(featuresets)
print(classifier.pseudocode(depth=4))
print nltk.classify.accuracy(classifier, featuresets)

sentence = "Mark: is it ok?"
tokenized_sentence = nltk.word_tokenize(sentence)
for i, word in enumerate(tokenized_sentence):
    print "{0} -> {1}".format(word, classifier.classify(pos_features(tokenized_sentence, i)))
