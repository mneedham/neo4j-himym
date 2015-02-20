import nltk

sentence = "What was I doing? Your Uncle Marshall was taking the biggest step of his life, and me-I'm calling your Uncle, Barney."

sentences = nltk.sent_tokenize(sentence)
sentences = [nltk.word_tokenize(sent) for sent in sentences]
sentences = [nltk.pos_tag(sent) for sent in sentences]

# grammar = "NP: {<DT>?<JJ>*<NN>}"

# print sentences

grammar = '''
NP: {<DT>?<JJ>*<NN>*}
V: {<V.*>}'''

cp = nltk.RegexpParser(grammar)
result = cp.parse(sentences[0])

# for n in result:
#     if isinstance(n, nltk.tree.Tree):
#         if n.node == 'NP':
#             print n
#         else:
#             print n

grammar = r"""
  NP:
    {<.*>+}          # Chunk everything
    }<VBD|IN>+{      # Chink sequences of VBD and IN
  """

cp = nltk.RegexpParser(grammar)
result = cp.parse(sentences[0])
print result

for n in result:
    print n
