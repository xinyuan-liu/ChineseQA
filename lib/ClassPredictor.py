from __future__ import absolute_import
from __future__ import print_function
import numpy as np
np.random.seed(1337)  # for reproducibility

from keras.preprocessing import sequence
from keras.optimizers import SGD, RMSprop, Adagrad
from keras.utils import np_utils
from keras.models import Sequential
from keras.layers.core import Dense, Dropout, Activation, Reshape
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import LSTM, GRU
import pickle
import jieba

#pkl_file = open('pkl/query_train.pkl', 'rb')
#query_train = pickle.load(pkl_file)
batch_size = 32
weights_file='models/tag_predict.weight'
model = Sequential()
model.add(GRU(output_dim=128,input_dim = 400, activation='tanh', inner_activation='hard_sigmoid', input_length=40))
model.add(Dropout(0.5))
model.add(Dense(116, activation='softmax'))
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.load_weights(weights_file)
tag_dict=pickle.load(open('pkl/tag_dict.pkl','rb'))

def predict(query,gensim_dic,alter_num=3):
    X=[]
    x=[]
    wl=list(jieba.cut(query))
    for word in wl:
        if word in gensim_dic:
            x.append(gensim_dic[word])
        else:
            x.append([0 for i in range(400)])
    while len(x)<40:
        x.append([0 for i in range(400)])
    x=np.array(x)
    X.append(x)
    res=model.predict(np.array(X))
    l=[]
    for i in range(len(res[0])):
        l.append((res[0][i],i))
    l.sort()
    ans=[]
    i=0
    for pair in reversed(l):
        ans.append(tag_dict[pair[1]])
        i+=1
        if(i==alter_num):
            break
    return ans
