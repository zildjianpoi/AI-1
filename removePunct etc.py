# -*- coding: utf-8 -*-
"""
Created on Sun Sep  2 11:33:36 2018

@author: Chelsea Chen
"""

"""How to remove things from strings in one line"""
import string

a = input()
a = a.translate(str.maketrans('','',string.punctuation)).lower() #remove punctuation
print(a)

a = a.translate(str.maketrans('','', '0123456789')).lower() #remove numbers
print(a)

"""Finding cases of things"""
import re
pattern = input()
string = input() #string to look 4 the pattern
s = '(?=' + pattern + ')'
l = [m.start() for m in re.finditer(str(s), string)] 
"""re.finditer = iterator over smthing"""
#   start index of m, where m equals ---(forloop) --- re.finditer (pattern, string, flags???) 
print(l) #the start indexes of each case of