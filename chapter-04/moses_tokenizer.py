#!/usr/bin/env python
# coding: utf-8

# In[9]:


# import nltk
# nltk.download('perluniprops')
# nltk.download('nonbreaking_prefixes')
import sys, fileinput
from nltk.tokenize.moses import MosesTokenizer

t= MosesTokenizer()

if __name__=="__main__":
    for line in fileinput.input():
        if line.strip() !='':
            tokens = t.tokenize(line.strip(), escape = False)
            
            sys.stdout.write(' '.join(tokens) + '\n')
            
        else:
            sys.stdout.write('\n')

