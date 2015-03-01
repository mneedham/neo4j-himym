def pos_features(sentence, sentence_pos, i):
    features = {}

    features["word"] = sentence[i]
    features["word-pos"] = sentence_pos[i][1]

    if i == 0:
        features["prev-word"] = "<START>"
        features["prev-word-pos"] = "<START>"
    else:
        features["prev-word"] = sentence[i-1]
        features["prev-word-pos"] = sentence_pos[i-1]

    if i == len(sentence) - 1:
        features["next-word"] = "<END>"
        features["next-word-pos"] = "<END>"
    else:
        features["next-word"] = sentence[i+1]
        features["next-word-pos"] = sentence_pos[i+1]

    return features
