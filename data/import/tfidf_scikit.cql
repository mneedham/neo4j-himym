// phrases
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 0 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 100000 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 200000 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 300000 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 400000 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 500000 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 600000 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 700000 LIMIT 100000
MERGE (phrase:Phrase {value: row.Phrase});

// phrases -> episodes
LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 0 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 100000 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 200000 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 300000 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 400000 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 500000 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 600000 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);

LOAD CSV WITH HEADERS FROM "file:///Users/markneedham/projects/neo4j-himym/data/import/tfidf_scikit.csv" AS row
WITH row SKIP 700000 LIMIT 100000
MATCH (phrase:Phrase {value: row.Phrase})
MATCH (episode:Episode {id: toInteger(row.EpisodeId)})
MERGE (phrase)-[:USED_IN_EPISODE {tfidfScore: TOFLOAT(row.Score)}]->(episode);
