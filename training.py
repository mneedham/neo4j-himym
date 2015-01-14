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
        self.current_sentence = self.sentences[randint(0, len(sentences))]
        self.prompt = self.current_sentence['Sentence'] + " : "
        return Cmd.onecmd(self, s)

    def __init__(self, sentences):
        Cmd.__init__(self)
        self.sentences = sentences

    def do_no(self, line):
        with open("data/import/sentences_training.csv", 'a') as training_file:
            writer = csv.writer(training_file, delimiter=",")
            writer.writerow([self.previous_sentence["SentenceId"], "no"])

    def do_yes(self, line):
        with open("data/import/sentences_training.csv", 'a') as training_file:
            writer = csv.writer(training_file, delimiter=",")
            writer.writerow([self.previous_sentence["SentenceId"], "yes"])


    def do_EOF(self, line):
        return True

if __name__ == '__main__':
    sentences = []
    with open("data/import/sentences.csv", 'r') as sentences_file:
        reader = csv.DictReader(sentences_file, delimiter=",")
        for sentence in reader:
            sentences.append(sentence)
    app = App(sentences)
    app.cmdloop()
