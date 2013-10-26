from __future__ import division
from math import log
import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize

import pronounce

def log2(x): return log(x) / log(2)

infinity = float('Inf')

def score(phrase):
    "Lower scores mean more alliteration. But it's really super-crude."
    if not phrase: return infinity
    blah = [pronounce.phonetic(word).split() for word in phrase]
    goober = [first_consonant(phones) for phones in blah]
    counter = Counter(goober)
    total = sum(counter.values())
    entropy = sum(-count/total * log2(count/total)
                  for key, count in counter.items())
#    return entropy / len(phrase), counter
    return entropy, counter

def first_consonant(phones):
#    return phones[0]
    for phone in phones:
        if not pronounce.is_vowel(phone):
            return phone
    return ''

def score_em_all(filename):
    with open(filename) as f:
        text = f.read()
        for line in sent_tokenize(text):
            line = line.replace('\r', ' ').replace('\n', ' ')
#            import sys
            words = get_words(line)
#            sys.stderr.write(repr(words) + '\n')
            try:
                nonalliterativeness, counter= score(words)
                if nonalliterativeness < infinity:
                    print nonalliterativeness, counter, line
            except KeyError:
#                print 'oops', words
                pass

def get_words(text):
    "Return text's words in order."
    return [word.strip("'") for word in re.findall(r"['\w]+", text)]

if __name__ == '__main__':
    score_em_all('great-expectations.txt')

## score('when in the course of human events'.split())
#. (2.5216406363433186, Counter({'IH0': 2, 'DH': 1, 'K': 1, 'HH': 1, 'AH1': 1, 'W': 1}))
## score('peter piper picked a peck'.split())
#. (0.7219280948873623, Counter({'P': 4, 'AH0': 1}))
## score('peter piper picked a really random rule'.split())
#. (1.4488156357251847, Counter({'P': 3, 'R': 3, 'AH0': 1}))
## score('peter piper picked a different stupid zoo'.split())
#. (2.128085278891395, Counter({'P': 3, 'S': 1, 'AH0': 1, 'Z': 1, 'D': 1}))
