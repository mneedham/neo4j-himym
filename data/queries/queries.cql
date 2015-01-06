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
