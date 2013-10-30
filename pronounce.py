from __future__ import division
import itertools
import re

phone_dict = {}
for line in open('cmudict.0.7a'):
    if ';;' in line: continue
    s = line.split()
    if not s: continue
    word, phones = s[0], s[1:]
    phone_dict[word] = tuple(phones)

vowels = frozenset('AA AE AH AO AW AY EH ER EY IH IY OW OY UH UW'.split())

def is_vowel(phone):
    return phone[-1] in '012'

def pronounce(word):
    key = word.upper()
    try:
        return phone_dict[key]
    except KeyError:
        #if key.endswith("'S"):
            #return phone_dict[key[:-2]] + ('Z',)
        raise

## pronounce("carrie's")
#. ('K', 'EH1', 'R', 'IY0', 'Z')

def phonetic(word):
    return ' '.join(pronounce(word))

def known_words():
    return phone_dict.iterkeys()

def is_pronouncing_ambiguous(key):
    return key + '(2)' in phone_dict

def main():
    import sys
    for line in sys.stdin:
        for word in re.findall(r"['\w]+", line):
            print phonetic(word)

def test():
    "See how many words can be pronounced"
    import scoring
    words = scoring.get_words(open("test-data.txt").read())
    pronouncables = []
    for word in words:
        try:
            if pronounce(word):
                pronouncables.append(word)
        except KeyError:
            None
    return len(pronouncables)/len(words)
# cmu standard: 0.97794822627
# Darius's posssessive exception 0.972195589645
#

if __name__ == '__main__':
    print test()
    #main()
