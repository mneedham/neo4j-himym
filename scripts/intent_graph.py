import requests
import csv
import time
import json

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimited(0.3)
def topics(title, body):
    payload = { 'title': title,
                'body': body,
                'api-token': "MTQyMzIxMDMyOTI5NA.cHJvZA.bS5oLm5lZWRoYW1AZ21haWwuY29t.8zicNYlnRSMduMv4jQFGARG-BMY"}
    r = requests.post("http://interest-graph.getprismatic.com/text/topic", data=payload)
    return r

episodes = {}
with open("data/import/episodes_full.csv", "r") as episodesfile:
    episodes_reader = csv.reader(episodesfile, delimiter=",")
    episodes_reader.next()
    for episode in episodes_reader:
        episodes[int(episode[0])] = {"title": episode[6], "sentences" : [] }

with open("data/import/sentences.csv", "r") as sentencesfile:
     sentences_reader = csv.reader(sentencesfile, delimiter=",")
     sentences_reader.next()
     for sentence in sentences_reader:
         episodes[int(sentence[1])]["sentences"].append(sentence[4])

with open("data/import/topics.csv", "w") as topicsfile:
    topics_writer = csv.writer(topicsfile, delimiter=",")
    topics_writer.writerow(["EpisodeId", "TopicId", "Topic", "Score"])

    for episode_id, episode in episodes.iteritems():
        tmp = topics(episode["title"], "".join(episode["sentences"])).json()
        print episode_id, tmp
        for topic in tmp['topics']:
            topics_writer.writerow([episode_id, topic["id"], topic["topic"], topic["score"]])
