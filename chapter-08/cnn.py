#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import torch 
import torch.nn as nn

class CNNClassifier(nn.Module):
    
    def __init__(self,
                input_size,
                word_vec_dim,
                n_classes,
                use_batch_norm = False,
                dropout_p = .5,
                window_size = [3,4,5],
                n_filters = [100,100,100]
                )
    
    self.input_size = input_size # vocabulary_size
    self.word_vec_dim = word_vec_dim
    self.n_classes = n_classes
    self.use_batch_norm = use_batch_norm
    self.dropout_p = dropout_p
    # window size means that how many words a pattern covers
    self.window_sizes = window_sizes
    # n_filters means how many patterns to cover
    self.n_filters = n_filters
    
    super().__init__()
    
    self.emb = nn.Embedding(input_size, word_vec_dim)
    # Since number of convolution layers would be vary depend on len(window_sizes),
    # we use 'setattr' and 'getattr' methods to add layers to nn.Module object.
    
    for window_size,n_filter in zip(window_sizes,n_filters):
        cnn = nn.Conv2d(in_channels=1,
                       out_channels=n_filter,
                       kernel_size=(window_size, word_vec_dim)
                       )
        setattr(self,'cnn-%d-%d' % (window_size,n_filter),cnn)
        
        if use_batch_norm:
            bn = nn.BatchNorm2d(n_filter)
            setattr(self,'bn-%d-%d' % (window_size,n_filter),bn)
        
        # Because below layers are just operations,
        # (it does not have learnable parameters)
        # we just declare once.
        
        if not use_batch_norm:
            self.drop_out = nn.Dropout(dropout_p)
        self.relu = nn.ReLU()
        # An input of generator layer is max values from each filter.
        self.generator = nn.Linear(sum(n_filters),n_classes)
        # We use LogSoftmax + NLLLoss instead of Softmax + CrossEntropy
        self.activation = nn.LogSoftmax(dim=-1)
        
    def forward(self,x):
        # |x| = (batch_size, length)
        x = self.emb(x)
        # |x| = (batch_size, length, word_vec_dim)
        min_length = max(self.window_sizes)
        if min_length > x.size(1):
            # Because some input does not long enough for maximum length of window size,
            # we add zero tensor for padding.
            pad = x.new(x.size(0), min_length - x.size(1), self.word_vec_dim).zero_()
            # |pad| = (batch_size, min_length - length, word_vec_dim)
            x = torch.cat([x,pad],dim=1)
            # |x| = (batch_size, min_length, word_vec_dim)
            
        # In ordinary case of vision task, you may have 3 channels on tensor,
        # but in this case, you would have just 1 channel,
        # which is added by 'unsqueeze' method in below:
        x = x.unsqueeze(1)
        # |x| = (batch_size, 1,length,word_vec_dim)
        
        cnn_outs = []
        for window_size, n_filter in zip(self.window_sizes, self.n_filters):
            cnn = getattr(self, 'cnn-%d-%d' % (window_size,n_filter))
            if self.use_batch_norm:
                bn = getattr(self,'bn-%d-%d' % (window_size,n_filter))
                cnn_out = bn(self.relu(cnn(x)))
            else:
                cnn_out = self.dropout(self.relu(cnn(x)))
            # |cnn_out| = (batch_size, n_filter, length - window_size +1, 1)
            
            # In case of max pooling, we does not know the pooling size,
            # because it depends on the length of the sentence.
            # Therefore, we use instant function using 'nn.functional' package.
            # This is the beauty of PyTorch.
            cnn_out = nn.functional.max_pool1d(input = cnn_out.squeeze(-1),
                                              kernel_size= cnn_out.size(-2)
                                              ).squeeze(-1)
            # |cnn_out| = (batch_size,n_filter)
            cnn_outs += [cnn_out]
        
        # Merge output tensors from each convolution layer.
        cnn_outs = torch.cat(cnn_outs, dim=-1)
        # |cnn_outs| = (batch_size, sum(n_filters))
        y = self.activation(self.generator(cnn_outs))
        # |y| = (batch_size,n_classes)
        
        return y
                                                        

