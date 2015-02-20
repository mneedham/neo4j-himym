from nltk.tag.stanford import NERTagger

st = NERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')

print st.tag('You can call me Billiy Bubu and I live in Amsterdam.'.split())
