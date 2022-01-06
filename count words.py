# -*- coding: utf-8 -*-
"""
Created on Sun Sep 16 14:38:21 2018

@author: Chelsea Chen
"""

import string
#count words
a = input("Passage: ").strip().split()
d = {}
for word in a:
    word = word.translate(str.maketrans('','',string.punctuation)).lower().translate(str.maketrans('','', '0123456789'))
    if not (word == "\n" or word == " " or word == "" or word == "and" or word == "in" or word == "is" or word == "the" or word == "to" or word == "of" or word == "a"):
        if word in d:
            d[word] = d[word] + 1
        else:
            d[word] = 1
print(d)
print(str(sorted(d.values())))

