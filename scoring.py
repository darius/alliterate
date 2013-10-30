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
    if not items: return infinity
    counter = Counter(map(func, items))
    return entropy(counter)

#def score_em_all(filename):
    #with open(filename) as f:
        #text = f.read()
    #for sentence in sent_tokenize(text):
        #sentence = ' '.join(sentence.splitlines())
        #words = get_words(sentence)
        #if len(words) == 1: continue
        #try:
            #nonalliterativeness, counter = score(words, first_consonant)
        #except KeyError:
            #pass
        #else:
            #if nonalliterativeness < infinity:
                #yield nonalliterativeness, counter, sentence


#def entropy_of_sentence(sentence):
   #new_line_stripped_sentence = ' '.join(sentence.splitlines())
   #return entropy(Counter(get_words(new_line_stripped_sentence.lower()))), new_line_stripped_sentence

#def entropy_of_window(window):
  #return entropy(Counter(window))

#def multi_score_window(window):
    #try: 
       #first_consonant_e = score(window, first_consonant)[0]
       #sound_e = score(window, )
       #word_e = entropy_of_window(window)
       #try:
         #combined_e = pow(first_consonant_e, 3)  / word_e
       #except ZeroDivisionError:
           #combined_e = infinity
       #return (combined_e, first_consonant_e, word_e, " ".join(window), Counter(window))
    #except KeyError:
       #pass


   #word_phones = [pronounce.phonetic(word).split() for word in phrase]

if __name__ == '__main__':
    with open('great-expectations.txt') as f:
      text = f.read()
      for line in sorted([(score(window, first_consonant)," ".join(window)) for window in sliding_windows(get_words(text.lower()), 8)]):
          print line
      
      #for line in sorted([x for x in [multi_score_window(window) for window in sliding_windows(words)] if x is not None])[:10]:
          #print line[3]

## score('when in the course of human events'.split())
#. (2.5216406363433186, Counter({'V': 2, 'DH': 1, 'K': 1, 'N': 1, 'HH': 1, 'W': 1}))
## score('peter piper picked a peck'.split())
#. (0.7219280948873623, Counter({'P': 4, '': 1}))
## score('peter piper picked a really random rule'.split())
#. (1.4488156357251847, Counter({'P': 3, 'R': 3, '': 1}))
## score('peter piper picked a different stupid zoo'.split())
#. (2.128085278891395, Counter({'P': 3, '': 1, 'S': 1, 'Z': 1, 'D': 1}))




