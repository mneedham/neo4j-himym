#!/bin/bash

# https://gist.github.com/troyane/c9355a3103ea08679baf

echo " . . . Downloading file stanford-ner-2014-08-27.zip"
# NOTE: need to update link for further versions
wget http://nlp.stanford.edu/software/stanford-ner-2014-08-27.zip

echo " . . . Unpacking stanford-ner-2014-08-27.zip"
unzip stanford-ner-2014-08-27.zip

mkdir stanford-ner
cp stanford-ner-2014-08-27/stanford-ner.jar stanford-ner/stanford-ner.jar
cp stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.crf.ser.gz stanford-ner/english.all.3class.distsim.crf.ser.gz
cp stanford-ner-2014-08-27/classifiers/english.all.3class.distsim.prop stanford-ner/english.all.3class.distsim.prop

echo " . . . Clearing all"
rm -rf stanford-ner-2014-08-27 stanford-ner-2014-08-27.zip

echo " . . . Preparing Python test file test_sner.py"
touch test_sner.py
# import Stanford NER for NLTK (avaaible from 2.0 ver)
echo "from nltk.tag.stanford import NERTagger" >> test_sner.py
# initialize SNER using copied files
echo "st = NERTagger('stanford-ner/english.all.3class.distsim.crf.ser.gz', 'stanford-ner/stanford-ner.jar')" >> test_sner.py
# add test to see weather it works
echo "print st.tag('You can call me Billiy Bubu and I live in Amsterdam.'.split())" >> test_sner.py

chmod +x test_sner.py

echo " . . . Executing Python test file test_sner.py"
python test_sner.py

echo " . . . Isn't it cool? :)"
