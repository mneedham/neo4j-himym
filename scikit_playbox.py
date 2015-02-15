from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
import csv

episodes = defaultdict(list)
with open("data/import/sentences.csv", "r") as sentences_file:
    reader = csv.reader(sentences_file, delimiter=',')
    reader.next()
    for row in reader:
        episodes[row[1]].append(row[4])

for episode_id, text in episodes.iteritems():
    episodes[episode_id] = "".join(text)

cv = CountVectorizer(analyzer='word', ngram_range=(2,3), min_df = 0)

corpus = []
for id, episode in sorted(episodes.iteritems(), key=lambda t: int(t[0])):
    corpus.append(episode)

td_matrix =  cv.fit_transform(corpus)


tf_transformer = TfidfTransformer(use_idf=False).fit(td_matrix)
td_tfidf = tf_transformer.transform(td_matrix)
