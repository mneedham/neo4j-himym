import pandas as pd
df = pd.read_csv('data/import/tfidf_scikit.csv', index_col=False, header=0)

print ("Top 3 phrases by episode")
print("")
# Top 3 phrases for each episode
top_words_by_episode = df \
    .sort(["EpisodeId", "Score"], ascending = [True, False]) \
    .groupby(["EpisodeId"], sort = False) \
    .head(3)

print(top_words_by_episode.to_string())

print ("Top phrases in an episode")
print("")
# Top phrases in an episode
top_words = df[(df["EpisodeId"] == 1)] \
    .sort(["Score"], ascending = False) \
    .head(20)

print(top_words.to_string())

print ("Which episodes don't mention Robin by name?")
print("")
# Which episodes don't mention Robin by name?
all_episodes = set(range(1, 209))
robin_episodes = set(df[(df["Phrase"] == "robin")]["EpisodeId"])
print(set(all_episodes) - set(robin_episodes))

print ("How many of the top ten phrases were used in other episodes?")
print("")
# How many of the top ten phrases were used in other episodes?
phrases_used = set(df[(df["EpisodeId"] == 1)] \
    .sort(["Score"], ascending = False) \
    .head(10)["Phrase"])

phrases = df[df["Phrase"].isin(phrases_used)]

print (phrases[phrases["EpisodeId"] != 1] \
    .groupby(["Phrase"]) \
    .size() \
    .order(ascending = False))
