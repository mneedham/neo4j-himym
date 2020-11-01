// phrases
USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/words_scikit.csv" AS row
MERGE (phrase:Phrase {value: row.Phrase});

// episode -> phrase
USING PERIODIC COMMIT 1000
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/words_scikit.csv" AS row
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (episode)-[:CONTAINED_PHRASE {times:toInteger(row.Count)}]->(phrase);
