#!/bin/sh

for i in {1..9}; do wget "http://www.imdb.com/title/tt0460649/episodes?season="$i -O "data/season-${i}"; done
