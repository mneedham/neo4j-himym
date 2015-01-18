import csv
from phrasecounter import PhraseCounter

if __name__ == "__main__":
    phrase_counter = PhraseCounter()

    with open("data/import/sentences.csv", "r") as sentencesfile:
        reader = csv.reader(sentencesfile, delimiter=",")
        reader.next()
        count = 0
        for sentence in reader:
            if count > 5000:
                break
            phrase_counter.extract_phrases(sentence[4], 3)
            count = count + 1

    most_common_phrases = phrase_counter.most_common(500)
    for phrase,count in most_common_phrases:
        print '{0: <5}'.format(count), phrase
