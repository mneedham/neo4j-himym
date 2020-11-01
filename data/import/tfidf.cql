// words
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/words.csv" AS row
MERGE (word:Word {value: row.Word});

// words to episodes
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/words.csv" AS row
MATCH (word:Word {value: row.Word})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (word)-[:USED_IN_EPISODE {occurrences : toInteger(row.Occurrences)}]->(episode);


// tfidf words
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/words_tfidf.csv" AS row
MERGE (word:Word {value: row.Word});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/words_tfidf.csv" AS row
MATCH (word:Word {value: row.Word})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (word)-[:USED_IN_EPISODE {score : TOFLOAT(row.Score)}]->(episode);
