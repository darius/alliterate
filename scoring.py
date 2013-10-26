from __future__ import division
from math import log
import pronounce
from collections import Counter

def log2(x): return log(x) / log(2)

def score(phrase):
    "Lower scores mean more alliteration. But it's really super-crude."
    blah = [pronounce.phonetic(word).split() for word in phrase]
    goober = [phones[0] for phones in blah]
    counter = Counter(goober)
    total = sum(counter.values())
    entropy = sum(-count/total * log2(count/total)
                  for key, count in counter.items())
    return entropy

#    print key, count, count/total
## score('when in the course of human events'.split())
#. 2.5216406363433186
## score('peter piper picked a peck'.split())
#. 0.7219280948873623
