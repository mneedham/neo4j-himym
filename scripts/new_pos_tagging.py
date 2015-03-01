from textblob import TextBlob
from textblob_aptagger import PerceptronTagger

from himymutil.sentences import all_sentences
import functools
import time
import nltk

def timeit(func):
    @functools.wraps(func)
    def newfunc(*args, **kwargs):
        startTime = time.time()
        func(*args, **kwargs)
        elapsedTime = time.time() - startTime
        print('function [{}] finished in {} ms'.format(
            func.__name__, int(elapsedTime * 1000)))
    return newfunc

@timeit
def get_textblob_tags(sentence):
    blob = TextBlob(sentence, pos_tagger=PerceptronTagger())
    return blob.tags

@timeit
def get_nltk_tags(sentence):
    return nltk.pos_tag(sentence)

for sentence in all_sentences()[:10]:
    get_textblob_tags(sentence)
    get_nltk_tags(sentence)
