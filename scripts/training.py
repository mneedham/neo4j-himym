from cmd import Cmd
import csv
from random import randint

class App(Cmd):
    """Training data"""
    current_sentence = {}
    previous_sentence = {}
    prompt = 'You will see a sentence. Type "yes" if it contains a speaker and "no" if not'

    def onecmd(self, s):
        self.previous_sentence = self.current_sentence

        while True:
            potential_next = self.sentences[randint(0, len(sentences))]
            if potential_next["SentenceId"] not in self.trained:
                self.current_sentence = potential_next
                break
            else:
                print "%s Seen already" % (potential_next["SentenceId"])

        self.prompt = self.current_sentence['Sentence'] + " : "
        return Cmd.onecmd(self, s)

    def __init__(self, sentences, trained):
        Cmd.__init__(self)
        self.sentences = sentences
        self.trained = trained

    def do_no(self, line):
        with open("data/import/sentences_training.csv", 'a') as training_file:
            writer = csv.writer(training_file, delimiter=",")
            writer.writerow([self.previous_sentence["SentenceId"], "no"])
            self.trained.add(self.previous_sentence["SentenceId"])

    def do_yes(self, line):
        with open("data/import/sentences_training.csv", 'a') as training_file:
            writer = csv.writer(training_file, delimiter=",")
            writer.writerow([self.previous_sentence["SentenceId"], "yes"])
            self.trained.add(self.previous_sentence["SentenceId"])


    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    sentences = []
    with open("data/import/sentences.csv", 'r') as sentences_file:
        reader = csv.DictReader(sentences_file, delimiter=",")
        for sentence in reader:
            sentences.append(sentence)

    trained = set()
    with open("data/import/sentences_training.csv", 'r') as training_file:
        reader = csv.DictReader(training_file, delimiter=",")
        for sentence in reader:
            trained.add(sentence["SentenceId"])
    print len(trained)

    app = App(sentences, trained)
    app.cmdloop()
