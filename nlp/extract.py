import lxml.html
from lxml.cssselect import CSSSelector
import nltk
import re

def tnes(text):
  tokens = []
  # split the source string into a list of sentences
  # for each sentence, split it into words and tag the word with its PoS
  # send the words to the named entity chunker
  # for each chunk containing a Named Entity, build an nltk Tree consisting of the word and its Named Entity tag
  # and append it to the list of tokens for the sentence
  # for each chunk that does not contain a NE, add the word to the list of tokens for the sentence
  for sentence in nltk.sent_tokenize(text):
    for chunk in nltk.ne_chunk(nltk.pos_tag(nltk.word_tokenize(sentence))):
      if hasattr(chunk,  'node'):
        print chunk
        tmp_tree = nltk.Tree("PERSON",  [(' '.join(c[0] for c in chunk.leaves()))])
        tokens.append(tmp_tree)
      else:
        tokens.append(chunk[0])
  return tokens

def tnes2(cp, text):
  tokens = []
  # split the source string into a list of sentences
  # for each sentence, split it into words and tag the word with its PoS
  # send the words to the named entity chunker
  # for each chunk containing a Named Entity, build an nltk Tree consisting of the word and its Named Entity tag
  # and append it to the list of tokens for the sentence
  # for each chunk that does not contain a NE, add the word to the list of tokens for the sentence
  for sentence in nltk.sent_tokenize(text):
    for chunk in cp.parse(nltk.pos_tag(nltk.word_tokenize(sentence))):
      if hasattr(chunk,  'node'):
        tmp_tree = nltk.Tree("PERSON",  [(' '.join(c[0] for c in chunk.leaves()))])
        tokens.append(tmp_tree)
      else:
        tokens.append(chunk[0])
  return tokens


f = open('data/Pilot.html', 'r')

tree = lxml.html.fromstring(f.read())

sel = CSSSelector('div.mw-content-ltr p')
results = sel(tree)

# first paragraph
results[5].text_content()

sentence = results[5].text_content()
tagged_sentence = nltk.pos_tag(nltk.word_tokenize(sentence))

grammar = r"""
NP: {<NN.>?}
"""

cp = nltk.RegexpParser(grammar)
cp.parse(tagged_sentence)

IN = re.compile (r'.*\b.*\b')
class doc():
  pass

doc.headline = ['this is expected by nltk.sem.extract_rels but not used in this script']
doc.text = tnes(sentence)

print "find rels"
for rel in  nltk.sem.extract_rels('PERSON','PERSON',doc,corpus='ieer',pattern=IN):
   print nltk.sem.relextract.show_raw_rtuple(rel)

doc.headline = ['this is expected by nltk.sem.extract_rels but not used in this script']
doc.text = tnes2(cp, sentence)




match = results[2]
# print lxml.html.tostring(match)

# find dem links - these are effectively entities in the series
CSSSelector('a')(results[5])
