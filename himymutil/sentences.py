import csv

def all_sentences():
    all_sentences = []
    with open("data/import/sentences.csv", "r") as sentences_file:
        reader = csv.reader(sentences_file, delimiter = ",")
        reader.next()
        for row in reader:
            all_sentences.append(row[4])
    return all_sentences
