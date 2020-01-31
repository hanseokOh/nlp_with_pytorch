#!/usr/bin/env python
# coding: utf-8

'''
한 줄에서 클래스와 텍스트가 탭('\t')으로 구분된 데이터의 입력을 받음
주로 텍스트 분류를 위한 예제
'''
from torchtext import data

class DataLoader(object):
    
    def __init__(self,train_fn,valid_fn,
                batch_size = 64,
                device = -1,
                max_vocab = 999999,
                min_freq = 1,
                use_eos = False,
                shuffle = True
                ):
        super(DataLoader,self).__init__()
        
        # Define field of the input file
        # The input file consists of two fields.
        self.label = data.Field(sequential = False,
                               use_vocab = True,
                               unk_token = None
                               )
        self.text = data.Field(use_vocab = True,
                              batch_first= True,
                              include_lengths = False,
                              eos_token='<EOS>' if use_eos else None
                              )
        
        # Those defined two columns will be delimited by TAB.
        # Thus, we use TabularDataset to load two columns in the input file.
        # We would have two separate input file: train_fn, valid_fn
        # Files consists of two columns : label filed and text field.
        train, valid = data.TabularDataset.splits(path='',
                                                 train = train_fn,
                                                 validation = valid_fn,
                                                 format ='tsv',
                                                 fields = [('label', self.label),
                                                          ('text',self.text)
                                                          ]
                                                 )
        # Those loaded dataset would be feeded into each iterator:
        # train iterator and valid iterator.
        # We sort input sentences by length, to group similar lengths.
        self.train_iter, self.valid_iter = data.BucketIterator.splits((train,valid),
                                                                     batch_size = batch_size,
                                                                     device = 'cuda:%d' % device if device >=0 else 'cpu',
                                                                     shuffle= shuffle,
                                                                     sort_key = lambda x:len(x.text),
                                                                     sort_within_batch = True
                                                                     )
        # At last, we make a vocabulary for label and text field.
        # It is making mapping table between words and indice.
        self.label.build_vocab(train)
        self.text.build_vocab(train,max_size=max_vocab,min_freq=min_freq)
        

