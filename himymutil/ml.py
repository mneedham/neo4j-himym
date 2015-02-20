
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
