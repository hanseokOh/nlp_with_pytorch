#!/usr/bin/env python
# coding: utf-8


'''
기존의 공백과 전처리 단계에서 생성된 공백을 서로 구분하기 위한 특수문자 "__"을 삽입 예제
'''
import sys

STR =  '▁'

if __name__ =="__main__":
    ref_fn = sys.argv[1] #argparse와 같이 command 창의 입력 값을 index로 접근 가능
    
    f = open(ref_fn, 'r')
    
    for ref in f:
        ref_tokens = ref.strip().split(' ') # argv[1]을 통해서 넣는 전처리 전의 corpus 
        input_line = sys.stdin.readline().strip() #ref_tokens와 비교할 전처리 후의 corpus
        
        if input_line != '':
            tokens = input_line.split(' ')
            
            idx =0
            buf = []
            
            # We assume that stdin has more tokens than reference input.
            for ref_token in ref_tokens:
                tmp_buf =[]
                
                while idx <len(tokens):
                    if tokens[idx].strip() =='':
                        idx +=1
                        continue
                
                    tmp_buf +=[tokens[idx]]
                    idx +=1
                    
                    if ''.join(tmp_buf) == ref_token:
                        break
                        
                if len(tmp_buf)>0:
                    buf +=[STR + tmp_buf[0].strip()] + tmp_buf[1:]
                    
            sys.stdout.write(' '.join(buf) + '\n')
        
        else:
            sys.stdout.write('\n')
    
    f.close()

