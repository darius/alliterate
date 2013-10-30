from __future__ import division
from collections import Counter
from math import log
import re

import pronounce

infinity = float('Inf')

def log2(x): return log(x, 2)

def first_consonant(phones):
    for phone in phones:
        if not pronounce.is_vowel(phone):
            return phone
    return ''

def sliding_windows(input, n=8):
  return [input[i:i+n] for i in range(len(input)-n+1)]

def entropy(counter):
    "Shannon's Information Theory Entropy Score"
    total = sum(counter.values())
    if 0 == total: return 0
    return sum(-count/total * log2(count/total)
               for count in counter.values())

def get_words(text):
    "Return text's words in order."
    return [word.strip("'") for word in re.findall(r"['\w]+", text)]

def score(items, func):
    "Lower scores mean more alliteration. But it's really super-crude."
    return entropy(Counter(map(func, items)))

def test(s):
    return score(s.split(),
                 lambda word: first_consonant(pronounce.pronounce(word)))

## test('peter piper picked a peck')
#. 0.7219280948873623

## test('peter piper picked a really random rule')
#. 1.4488156357251847

## test('peter piper picked a different stupid zoo')
#. 2.128085278891395

## test('when in the course of human events')
#. 2.5216406363433186

def first_consonant_entropy(words):
    return entropy(Counter(first_consonant(pronounce.pronounce(word))
                           for word in words))

def word_entropy(words):
    return entropy(Counter(words))

def boringness(words):
    try:
       return first_consonant_entropy(words) / word_entropy(words)
    except (KeyError, ZeroDivisionError):
       return infinity

if __name__ == '__main__':
    with open('test-data.txt') as f:
      text = f.read()
    words = get_words(text.lower())
    for result in sorted([(boringness(window), ' '.join(window))
                          for window in sliding_windows(words, 8)]):
        print result
