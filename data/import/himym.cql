// episodes
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/episodes_full.csv" AS row
MERGE (episode:Episode {id: TOINT(row.NumberOverall)})
SET episode.title = row.Title,
    episode.viewers = toFloat(row.Viewers),
    episode.dateAired = row.DateAired,
    episode.timestamp = TOINT(row.Timestamp),
    episode.number = TOINT(row.NumberInSeason),
    episode.season = TOINT(row.Season),
    episode.ranking = TOINT(row.Rating);

// directors
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/episodes_full.csv" AS row
MERGE (person:Person {name: row.Director});

// writers
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/episodes_full.csv" AS row
WITH split(row.Writers, ",") AS writers
UNWIND writers AS writer
WITH DISTINCT writer
MERGE (person:Person {name: writer});

// seasons
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/episodes_full.csv" AS row
MERGE (season:Season {number: row.Season});

// directors -> episodes
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/episodes_full.csv" AS row
MATCH (person:Person {name: row.Director})
MATCH (episode:Episode {id: TOINT(row.NumberOverall)})
MERGE (person)-[:DIRECTED_EPISODE]->(episode);

// writers -> episodes
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/episodes_full.csv" AS row
MATCH (episode:Episode {id: TOINT(row.NumberOverall)})
WITH split(row.Writers, ",") AS writers, episode
UNWIND writers AS writer
MATCH (person:Person {name: writer})
MERGE (person)-[:WROTE_EPISODE]->(episode);

// seasons -> episodes
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/episodes_full.csv" AS row
MATCH (season:Season {number: row.Season})
MATCH (episode:Episode {id: TOINT(row.NumberOverall)})
MERGE (episode)-[:IN_SEASON]->(season);

// link episodes
MATCH (episode:Episode)
WITH episode
ORDER BY episode.id
WITH COLLECT(episode) AS episodes

FOREACH(i in RANGE(0, length(episodes)-2) |
FOREACH(n1 in [episodes[i]] | FOREACH(n2 in [episodes[i+1]] |
    MERGE (n1)-[:NEXT_EPISODE]->(n2))));

// link seasons
MATCH (season:Season)
WITH season
ORDER BY season.number
WITH COLLECT(season) AS seasons

FOREACH(i in RANGE(0, length(seasons)-2) |
FOREACH(n1 in [seasons[i]] | FOREACH(n2 in [seasons[i+1]] |
  MERGE (n1)-[:NEXT_SEASON]->(n2))));

// characters
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/characters.csv" AS row
MERGE (character:Character {name: row.Character});

// actors
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/characters.csv" AS row
MERGE (person:Person {name: row.Actor});

// actors -> characters
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/characters.csv" AS row
MATCH (person:Person {name: row.Actor})
MATCH (character:Character {name: row.Character})
MERGE (person)-[:PLAYS_CHARACTER]->(character);

// character -> episode
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/characters.csv" AS row
MATCH (episode:Episode {id: TOINT(row.EpisodeId)})
MATCH (character:Character {name: row.Character})
MERGE (character)-[:APPEARED_IN_EPISODE]->(episode);


// topics
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/topics.csv" AS row
MERGE (topic:Topic {id: TOINT(row.TopicId)})
ON CREATE SET topic.value = row.Topic;

// topic - episode
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/topics.csv" AS row
MATCH (topic:Topic {id: TOINT(row.TopicId)})
MATCH (episode:Episode {id: TOINT(row.EpisodeId)})
MERGE (episode)-[:TOPIC {score: TOFLOAT(row.Score)}]->(topic);
