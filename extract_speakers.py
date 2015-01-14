import csv
import nltk
import re
import bs4

from bs4 import BeautifulSoup, NavigableString
from soupselect import select
from nltk.corpus import stopwords
from collections import Counter
from nltk.tokenize import word_tokenize

def counterify(words):
    tally=Counter(words)
    return tally

episodes_dict = {}
speaker_regex = re.compile('([^:]+):(.*)')

def extract_speaker(sentence):
    speaker = speaker_regex.match(item)
    name = speaker.group(1) if speaker else None

    return (name, nltk.pos_tag(name.split(" ")))  if name else (None, None)

def strip_tags(soup, invalid_tags):
    for tag in invalid_tags:
        for match in soup.findAll(tag):
            match.replaceWithChildren()
    return soup

def extract_sentences(html):
    clean = []
    brs_in_a_row = 0
    temp = ""
    for item in raw_text.contents:
        if item.name == "br":
            brs_in_a_row = brs_in_a_row + 1
        else:
            temp = temp + item
        if brs_in_a_row == 2:
            clean.append(temp)
            temp = ""
            brs_in_a_row = 0
    return clean

speakers = []
with open('data/import/episodes.csv', 'r') as episodes_file, open("data/import/speakers.csv", 'w') as speakers_file:
    reader = csv.reader(episodes_file, delimiter=',')
    reader.next()

    writer = csv.writer(speakers_file, delimiter=',')
    writer.writerow(["Speaker", "Count"])

    for row in reader:
        transcript = open("data/transcripts/S%s-Ep%s" %(row[3], row[1])).read()
        # transcript = open("data/transcripts/S%s-Ep%s" %("1", "11")).read()
        soup = BeautifulSoup(transcript)
        rows = select(soup, "table.tablebg tr td.post-body div.postbody")

        raw_text = rows[0]
        [ad.extract() for ad in select(raw_text, "div.ads-topic")]
        [ad.extract() for ad in select(raw_text, "div.t-foot-links")]
        [ad.extract() for ad in select(raw_text, "hr")]

        for tag in ['strong', 'em', "a"]:
            for match in raw_text.findAll(tag):
                match.replace_with_children()
        print row
        speakers = speakers + [
            (extract_speaker(item))
            for item in [
                item.encode("utf-8").strip()
                for item in extract_sentences(raw_text.contents)
            ]
        ]

    speakers_count =  counterify(speakers)
    for speaker in speakers_count:
        writer.writerow([speaker, speakers_count[speaker]])
