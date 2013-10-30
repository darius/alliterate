from __future__ import division
from math import log, pow
import re
from collections import Counter
from nltk.tokenize import sent_tokenize

import pronounce

infinity = float('Inf')

def log2(x): return log(x, 2)

def first_consonant(phones):
    for phone in phones:
        try:
            if not pronounce.is_vowel(phone):
                return phone
            return ''
        except KeyError:
            pass

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
    if not items: return infinity
    counter = Counter(map(func, items))
    return entropy(counter)

def first_consontant_entropy(window):
    return entropy(Counter(map(first_consonant, [pronounce.phonetic(word).split() for word in window])))

def word_entropy(window):
    return entropy(Counter(window))

def total_entropy(window):
    try:
       return first_consontant_entropy(window) / word_entropy(window)
    except (KeyError, ZeroDivisionError):
       return infinity

if __name__ == '__main__':
    with open('test-data.txt') as f:
      text = f.read()
      for result in sorted([(total_entropy(window), " ".join(window)) for window in sliding_windows(get_words(text.lower()),8)]):
          print result
