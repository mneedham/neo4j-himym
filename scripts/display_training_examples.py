import csv
from collections import Counter

sentences = {}
speaker_counter = Counter()
sentence_counter = Counter()

with open("data/import/sentences.csv", "r") as sentencesfile, \
     open("data/import/sentences_training.csv", "r") as trainingfile:

    sentences_reader = csv.DictReader(sentencesfile, delimiter=",")
    for sentence in sentences_reader:
        sentences[sentence["SentenceId"]] = sentence

    training_reader = csv.DictReader(trainingfile, delimiter=",")
    for example in training_reader:
        sentence_id = example['SentenceId']
        sentence = sentences[sentence_id]
        contains_speaker = example["ContainsSpeaker"]
        sentence_text = sentence["Sentence"]

        speaker_counter[contains_speaker] += 1
        sentence_counter[sentence_id] += 1

        print "%s\n%s" % (sentence_text, contains_speaker)

print speaker_counter
print sentence_counter.most_common(10)
