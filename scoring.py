from __future__ import division
from math import log
import pronounce
from collections import Counter

def log2(x): return log(x) / log(2)

infinity = float('Inf')

def score(phrase):
    "Lower scores mean more alliteration. But it's really super-crude."
    if not phrase: return infinity
    blah = [pronounce.phonetic(word).split() for word in phrase]
    goober = [phones[0] for phones in blah]
    counter = Counter(goober)
    total = sum(counter.values())
    entropy = sum(-count/total * log2(count/total)
                  for key, count in counter.items())
    return entropy / len(phrase)

def score_em_all(filename):
    with open(filename) as f:
        for line in f:
            line = line.rstrip('\n')
            try:
                nonalliterativeness = score(line.split())
                if nonalliterativeness < infinity:
                    print nonalliterativeness, line
            except KeyError:
                pass

if __name__ == '__main__':
    score_em_all('great-expectations.txt')

#    print key, count, count/total
## score('when in the course of human events'.split())
#. 2.5216406363433186
## score('peter piper picked a peck'.split())
#. 0.7219280948873623
