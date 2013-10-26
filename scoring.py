from __future__ import division
from math import log
import re
from collections import Counter
from nltk.tokenize import sent_tokenize, word_tokenize

import pronounce

def log2(x): return log(x, 2)

infinity = float('Inf')

def score(phrase):
    "Lower scores mean more alliteration. But it's really super-crude."
    if not phrase: return infinity
    word_phones = [pronounce.phonetic(word).split() for word in phrase]
    counter = Counter(map(first_consonant, word_phones))
#    return entropy(counter) / len(phrase), counter
    return entropy(counter), counter

def first_consonant(phones):
#    return phones[0]
    for phone in phones:
        if not pronounce.is_vowel(phone):
            return phone
    return ''

def entropy(counter):
    total = sum(counter.values())
    if 0 == total: return 0
    return sum(-count/total * log2(count/total)
               for count in counter.values())

def score_em_all(filename):
    with open(filename) as f:
        text = f.read()
        for sentence in sent_tokenize(text):
            sentence = ' '.join(sentence.splitlines())
            words = get_words(sentence)
            try:
                nonalliterativeness, counter = score(words)
            except KeyError:
#                print 'oops', words
                pass
            else:
                if nonalliterativeness < infinity:
                    print nonalliterativeness, counter, sentence

def get_words(text):
    "Return text's words in order."
    return [word.strip("'") for word in re.findall(r"['\w]+", text)]

if __name__ == '__main__':
    score_em_all('great-expectations.txt')

## score('when in the course of human events'.split())
#. (2.5216406363433186, Counter({'V': 2, 'DH': 1, 'K': 1, 'N': 1, 'HH': 1, 'W': 1}))
## score('peter piper picked a peck'.split())
#. (0.7219280948873623, Counter({'P': 4, '': 1}))
## score('peter piper picked a really random rule'.split())
#. (1.4488156357251847, Counter({'P': 3, 'R': 3, '': 1}))
## score('peter piper picked a different stupid zoo'.split())
#. (2.128085278891395, Counter({'P': 3, '': 1, 'S': 1, 'Z': 1, 'D': 1}))
