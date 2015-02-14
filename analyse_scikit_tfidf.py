import pandas as pd
df = pd.read_csv('data/import/tfidf_scikit.csv', index_col=False, header=0)

df.groupby(["EpisodeId"]).max()


df.sort(["Score"], ascending = False).groupby(["EpisodeId"]).first()

# Top 3 words for each episode
top_words = df.sort(["Score"], ascending = False).groupby(["EpisodeId"], sort = False).head(3).sort(["EpisodeId", "Score"], ascending = [1, 0])
print(top_words.to_string())

# Top 20 for a specific episodes
top_words = df[(df["EpisodeId"] == 1)].sort(["Score"], ascending = False).head(20)
print(top_words.to_string())
