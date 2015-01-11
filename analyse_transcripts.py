import csv
import nltk
import re
import bs4

from bs4 import BeautifulSoup, NavigableString
from soupselect import select
from nltk.corpus import stopwords
from collections import Counter
from nltk.tokenize import word_tokenize

def count_words(words):
    tally=Counter()
    for elem in words:
        tally[elem] += 1
    return tally

episodes_dict = {}
speaker_regex = re.compile('([^:]+):(.*)')

def extract_speaker(sentence):
    speaker = speaker_regex.match(item)
    return speaker.group(1) if speaker else None

def strip_tags(soup, invalid_tags):
    for tag in invalid_tags:
        for match in soup.findAll(tag):
            match.replaceWithChildren()
    return soup

def merge_items(one, two):
    if type(two) is bs4.element.NavigableString and  two.startswith(":"):
        return one + two
    elif type(one) is bs4.element.NavigableString and one.startswith(":"):
        return None
    else:
        return one

with open('data/import/episodes.csv', 'r') as episodes:
    reader = csv.reader(episodes, delimiter=',')
    reader.next()

    count = 0
    for row in reader:
        if count > 1:
            break
        count = count + 1

        # transcript = open("data/transcripts/S%s-Ep%s" %(row[3], row[1])).read()
        transcript = open("data/transcripts/S%s-Ep%s" %("1", "11")).read()
        # transcript = open("data/transcripts/S%s-Ep%s" %("1", "1")).read()
        soup = BeautifulSoup(transcript)
        rows = select(soup, "table.tablebg tr td.post-body div.postbody")

        raw_text = rows[0]
        [ad.extract() for ad in select(raw_text, "div.ads-topic")]
        [ad.extract() for ad in select(raw_text, "div.t-foot-links")]
        [ad.extract() for ad in select(raw_text, "hr")]

        for tag in ['strong', 'em']:
            for match in raw_text.findAll(tag):
                match.replace_with_children()

        html = raw_text.prettify("utf-8")
        with open('/tmp/S1Ep11', 'wb') as handle:
            handle.write(html)

        sentences = [
            (extract_speaker(item), item)
            for item in [
                item.encode("utf-8").strip()
                for item in [
                    merge_items(one,two)
                    for one,two in zip(raw_text.contents, raw_text.contents[1:])
                ]
                if item is not None
            ]
            if item not in ["<br/>", "<br />"]
        ]

        print row
        print sentences
