import sys
import csv
from phrasecounter import PhraseCounter

if __name__ == "__main__":
    phrase_counter = PhraseCounter()

    with open("data/import/sentences.csv", "r") as sentencesfile:
        reader = csv.reader(sentencesfile, delimiter=",")
        reader.next()
        count = 0
        for sentence in reader:
            if count > 10000:
                break
            for n in range(3, 10):
                phrase_counter.extract_phrases_starting_with(sentence[4], sys.argv[1:][0], n)
            count = count + 1

    most_common_phrases = phrase_counter.most_common(500)
    for phrase,count in most_common_phrases:
        print '{0: <5}'.format(count), phrase
