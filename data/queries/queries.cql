// Writers who worked together
MATCH (episode:Episode)<-[r:WROTE_EPISODE]-(writer)
WITH episode, COLLECT(writer) AS writers, COUNT(r) AS numberOfWriters
WHERE numberOfWriters > 1
RETURN [w IN writers | w.name], COUNT(*) AS times
ORDER BY times DESC

// Longest wait between seasons
MATCH (season)<-[:IN_SEASON]-(episode:Episode)-[:NEXT_EPISODE]->(next)-[:IN_SEASON]->(nextSeason)
WHERE season <> nextSeason
RETURN episode.title, next.title, (next.timestamp - episode.timestamp) / 60 / 60 / 24 as gap, season.number, nextSeason.number
ORDER BY gap DESC


MATCH (season)<-[:IN_SEASON]-(episode:`Episode`)-[:NEXT_EPISODE]->(next)-[:IN_SEASON]->(nextSeason)
WHERE season <> nextSeason
RETURN episode.title, next.title, (next.timestamp - episode.timestamp) / 60 / 60 / 24 as gap, season.number, nextSeason.number
ORDER BY gap DESC

// How many episodes has each character appeared in?
MATCH (c:Character)-[:APPEARED_IN_EPISODE]->()
RETURN c.name, COUNT(*) AS times
ORDER BY times DESC
LIMIT 10

// Which episodes didn't feature the narrator?
MATCH (c:Character {name: "Narrator (voice)"}), (e:Episode)
WHERE NOT (c)-[:APPEARED_IN_EPISODE]->(e)
RETURN e

// Which actors play more than one character?
MATCH (p:Person)-[:PLAYS_CHARACTER]->(c)
WITH p, COLLECT(c.name) AS characters
WHERE LENGTH(characters) > 1
RETURN p.name, characters

// Which episodes should have been seen previously to follow this one?
MATCH (e:Episode {title: "No Tomorrow"})-[:REFERENCES]->(ref)-[:HAPPENED_IN]->(original)
RETURN ref, original

// When's the yellow umbrella mentioned?
MATCH (refEpisode)-[:REFERENCES]->(r:Reference)-[:HAPPENED_IN]->(episode)
WHERE r.text =~ "(?i).*yellow umbrella.*"
RETURN r, episode, refEpisode

// which words are mentioned most
MATCH (word:Word)-[r:USED_IN_EPISODE]->(episode)
RETURN word.value, COUNT(episode) AS episodes, SUM(r.times) AS occurrences
ORDER BY occurrences DESC
LIMIT 10

// in each episode which of the main characters is referenced most often

WITH ["Ted", "Barney", "Robin", "Lily", "Marshall"] as mainCharacters
MATCH (word:Word) WHERE word.value IN mainCharacters
MATCH (episode:Episode)<-[r:USED_IN_EPISODE]-(word)
WITH episode, word, r
ORDER BY episode.id, r.times DESC
WITH episode, COLLECT({word: word.value, times: r.times})[0] AS topWord
RETURN episode.id, topWord.word AS word, topWord.times AS occurrences
ORDER BY episode.id

// top words used in TF/IDF terms by the episode

MATCH (word:Word)-[rel:USED_IN_EPISODE]->(e)

WITH word, rel,e
ORDER BY word.value, e.id WHERE rel.score > 0.5

WITH word, MIN(rel.score) AS min, MAX(rel.score) AS max, AVG(rel.score) AS avg, COUNT(*)
AS episodesCount, COLLECT(e.id) AS episodes

RETURN word.value, min, max, avg, episodes, episodesCount
ORDER BY episodesCount DESC
LIMIT 100

// top words used in TF/IDF terms by the season

MATCH (word:Word)-[rel:USED_IN_EPISODE]->(e)-[:IN_SEASON]->(season)

WITH word, rel,season
ORDER BY word.value, season.value WHERE rel.score > 0.5

WITH word, MIN(rel.score) AS min, MAX(rel.score) AS max, AVG(rel.score) AS avg,
     COUNT(*) AS seasonsCount, COLLECT(season.number) AS episodes

RETURN word.value, min, max, avg, episodes, seasonsCount
ORDER BY seasonsCount DESC
LIMIT 100

// most popular topics
match (t:Topic)<-[:TOPIC]-()
RETURN t.value, COUNT(*) AS times
ORDER BY times DESC

// most frequently occurring topics by season
match (t:Topic)<-[:TOPIC]-()-[:IN_SEASON]->(season)
WITH season, t, COUNT(*) AS times
ORDER BY season.number, times DESC
RETURN season.number, COLLECT(t.value)[..5]
ORDER BY season.number

// writers who worked together

match (writer:Person)-[:WROTE_EPISODE]->()<-[:WROTE_EPISODE]-(otherWriter)
RETURN writer.name, otherWriter.name, COUNT(*) AS times
ORDER BY times DESC

// what topics do writers writer about?

PROFILE match (writer:Person)-[r:WROTE_EPISODE]->(e)
WITH writer, COLLECT(e) AS episodes
WITH writer, episodes, LENGTH(episodes) AS numberOfEpisodes
UNWIND episodes AS e
MATCH (e)-[:TOPIC]->(topic)
WITH writer, topic, COUNT(*) AS times, numberOfEpisodes
ORDER BY writer.name, times DESC
RETURN writer.name, COLLECT({topic: topic.value, times: times})[..5] AS topics, numberOfEpisodes
ORDER BY numberOfEpisodes DESC
