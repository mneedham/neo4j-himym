#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from bottle import post,get, run, static_file, template, redirect, request, response
from py2neo import Graph
from bs4 import BeautifulSoup, NavigableString
import json
from json import dumps
from soupselect import select
import csv
import nltk
from random import randint

graph = Graph()

all_sentences = []
with open("data/import/sentences.csv", "r") as sentences_file:
    reader = csv.reader(sentences_file, delimiter = ",")
    reader.next()
    for row in reader:
        all_sentences.append(row[4])

@get('/css/<filename:re:.*\.css>')
def get_css(filename):
    return static_file(filename, root="static", mimetype="text/css")


@get('/images/<filename:re:.*\.png>')
def get_image(filename):
    return static_file(filename, root="static", mimetype="image/png")

@get('/js/<filename:re:.*\.js>')
def get_js(filename):
    return static_file(filename, root="static", mimetype="application/javascript")

@get("/")
def get_index():
     redirect("/episodes")

@get("/episodes")
def get_episodes():
    """ List of all episodes.
    """
    statement = """\
    MATCH (e:Episode)
    RETURN e.id AS id, e.title as title, e.number as number, e.season as season
    ORDER BY id
    """
    return template("episodes", episodes=graph.cypher.execute(statement))

@get("/episodes/<episode_id>")
def get_episode(episode_id):
    """ Show specific episode
    """
    statement = """\
    MATCH (e:Episode {id: {episodeId}})-[r:TOPIC]->(topic)
    WITH e, r, topic ORDER BY r.score DESC
    RETURN e.id AS id, e.title as title, e.season AS season, e.number AS number,
           COLLECT({id: topic.id, name: topic.value, score: r.score}) AS topics
    ORDER BY id
    """

    episode = graph.cypher.execute(statement, {"episodeId": int(episode_id)})[0]

    season = episode["season"]
    number = episode["number"]

    sentences = []
    with open("data/import/sentences.csv", "r") as sentences_file:
        reader = csv.reader(sentences_file, delimiter = ",")
        reader.next()
        for row in reader:
            if int(row[1]) == int(episode['id']):
                sentences.append(row[4])

    transcript = open("data/transcripts/S%d-Ep%d" %(season, number)).read()
    soup = BeautifulSoup(transcript)
    rows = select(soup, "table.tablebg tr td.post-body div.postbody")

    return template("episode", episode = episode, transcript = rows[0], sentences = sentences)

@get("/topics/<topic_id>")
def get_topic(topic_id):
    """ Show specific topic
    """
    statement = """\
    MATCH (topic:Topic {id: {topicId}})<-[r:TOPIC]-(e)
    WITH e, r, topic ORDER BY r.score DESC
    RETURN topic.id AS id, topic.value as value,
           COLLECT({id: e.id, title: e.title, score: r.score}) AS episodes
    ORDER BY id
    """
    topic = graph.cypher.execute(statement, {"topicId": int(topic_id)})[0]

    return template("topic", topic = topic)

@get("/training")
def get_sentences_to_train():
    print request.headers['Accept']
    if "application/json" in request.headers['Accept']:
        sentences = {"sentences": []}
        for i in range(0, 10):
            sentences["sentences"].append(nltk.word_tokenize(all_sentences[randint(0, len(all_sentences))]))

        response.content_type = "application/json"
        return sentences
    else:
        return template("training")

@post("/training")
def train_sentence():
    print request.body
    with open("data/import/trained_sentences.json", "r") as json_file:
        json_data = json.load(json_file)
    print json_data

    for sentence in json.load(request.body):
        json_data.append( sentence )
    print json_data

    with open("data/import/trained_sentences.json", "w") as json_file:
        json.dump(json_data, json_file)

if __name__ == "__main__":
    run(host="localhost", port=8000, reloader=True, debug = True)
