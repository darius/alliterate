from __future__ import division
from math import log
import re
from collections import Counter

import pronounce

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
            words = get_words(line)
            try:
                nonalliterativeness = score(words)
                if nonalliterativeness < infinity:
                    print nonalliterativeness, line
            except KeyError:
                pass

def get_words(text):
    "Return text's words in order."
    return [word.strip("'") for word in re.findall(r"['\w]+", text)]

if __name__ == '__main__':
    score_em_all('great-expectations.txt')

## score('when in the course of human events'.split())
#. 0.3602343766204741
## score('peter piper picked a peck'.split())
#. 0.14438561897747246
## score('peter piper picked a really random rule'.split())
#. 0.20697366224645494
## score('peter piper picked a different stupid zoo'.split())
#. 0.30401218269877067
