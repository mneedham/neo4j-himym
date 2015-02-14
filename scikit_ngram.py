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

# corpus = ["Kids, I'm going to tell you an incredible story. The story of how I met your mother",
#           "Kids Are we being punished for something like your mother?"]
# for text in corpus:
#     print text
# print

td_matrix =  cv.fit_transform(corpus)

# for w in cv.get_feature_names():
#     print w

tf_transformer = TfidfTransformer(use_idf=False).fit(td_matrix)
td_tfidf = tf_transformer.transform(td_matrix)

tf = TfidfVectorizer(analyzer='word', ngram_range=(1,3), min_df = 0, stop_words = 'english')
tfidf_matrix =  tf.fit_transform(corpus)

columns = td_matrix.shape[0]

# extract the score for one word in the second document
# word_id = 42
# word = tf.get_feature_names()[word_id]
# score = tfidf_matrix[1].getcol(word_id).getrow(0).toarray()[0][0]
# print '{0: <5} {1: <20} {2}'.format(word_id, word, score)

feature_names = tf.get_feature_names()
with open("data/import/tfidf_scikit.csv", "w") as file:
    writer = csv.writer(file, delimiter=",")
    writer.writerow(["EpisodeId", "Phrase", "Score"])

    doc_id = 0
    for doc in tfidf_matrix.todense():
        print "Document %d" %(doc_id)
        word_id = 0
        for score in doc.tolist()[0]:
            if score > 0:
                word = feature_names[word_id]
                # print '{0: <25} {1}'.format(word.encode("utf-8"), score)
                writer.writerow([doc_id+1, word.encode("utf-8"), score])
            word_id +=1
        doc_id +=1
