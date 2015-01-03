#!/bin/sh

for i in {1..9}; do wget "http://www.imdb.com/title/tt0460649/episodes?season="$i -O "data/season-${i}"; done

wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-37/ -O data/tv-critic/season-1
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-69/ -O data/tv-critic/season-2
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-19/ -O data/tv-critic/season-3
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-20/ -O data/tv-critic/season-4
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-43/ -O data/tv-critic/season-5
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-54/ -O data/tv-critic/season-6
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-73/ -O data/tv-critic/season-7
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-8/ -O data/tv-critic/season-8
wget http://www.thetvcritic.org/reviews/comedies/how-i-met-your-mother/season-9/ -O data/tv-critic/season-9

wget http://transcripts.foreverdreaming.org/viewforum.php?f=177 -O data/transcripts/page-1
wget http://transcripts.foreverdreaming.org/viewforum.php?f=177&sid=64cb68b725cf4aca9a18237aef83d076&start=112 -O data/transcripts/page-2
