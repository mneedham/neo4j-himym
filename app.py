#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bottle import get, run, static_file, template
from py2neo import Graph
graph = Graph()

@get("/")
def get_index():
    """ List of all episodes.
    """
    statement = """\
    MATCH (e:Episode)
    RETURN e.id AS id, e.title as title
    ORDER BY id
    """
    return template("index", episodes=graph.cypher.execute(statement))

if __name__ == "__main__":
    run(host="localhost", port=8080, reloader=True)
