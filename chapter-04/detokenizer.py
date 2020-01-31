#!/usr/bin/env python
# coding: utf-8

# In[1]:


'''
분절 복원

sed "s/ //g" | sed "s/▁▁/ /g" | sed "s/▁//g" | sed "s/^\s//g"

의 스트림 편집 명령어와 같은 역할
'''

import sys

if __name__ =="__main__":
    for line in sys.stdin:
        if line.strip() !="":
            if '▁▁'in line:
                line = line.strip().replace(' ','').replace('▁▁',' ').replace('▁','').strip()
            else:
                line = line.strip().replace(' ','').replace('▁',' ').strip()
            sys.stdout.write(line +'\n')
            
        else:
            sys.stdout.write('\n')

