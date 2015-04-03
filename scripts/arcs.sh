#!/bin/bash

find_term() {
  arc=${1}
  searchTerm=${2}
  episodes=$(grep --color -iE "${searchTerm}" data/import/sentences.csv | awk -F"," '{ print $2  }' | sort | uniq)
  for episode in ${episodes}; do
    echo ${arc},${episode}
  done
}

find_term "Bro Code" "bro code"
find_term "Legendary" "legen(.*)ary"
find_term "Slutty Pumpkin" "slutty pumpkin"
find_term "Magician's Code" "magician's code"
find_term "Thanksgiving" "thanksgiving"
find_term "The Playbook" "playbook"
find_term "Slap Bet" "slap bet"
find_term "Wrestlers and Robots" "wrestlers"
find_term "Robin Sparkles" "sparkles"
find_term "Blue French Horn" "blue french horn"
find_term "Olive Theory" "olive"
find_term "Thank You Linus" "thank you, linus"
find_term "Have you met...?" "have you met"
find_term "Laser Tag" "laser tag"
find_term "Goliath National Bank" "goliath national bank"
find_term "Challenge Accepted" "challenge accepted"
find_term "Best Man" "best man"
