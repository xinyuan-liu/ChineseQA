import jieba
import numpy as np
import jieba.analyse

def get_key_words(str):
    return jieba.analyse.extract_tags(str)

def get_match_vec(word,query,word_list,window_size=5):
    x=np.zeros(window_size*2)
    key_words=get_key_words(query)
    l=len(word_list)
    for i in range(l):
        if word_list[i]==word:
            for j in range(window_size):
                if i+j+1 in range(l) and word_list[i+j+1] in key_words:
                    x[j]+=1
                if i-j-1 in range(l) and word_list[i-j-1] in key_words:
                    x[window_size+j]+=1
    return x

def get_word_frequency(possible_answer,word_list):
    word_freq=np.zeros(len(possible_answer))
    for w in word_list:
        if w in possible_answer:
            word_freq[possible_answer.index(w)]+=1
    return word_freq

def match(str1,str2):
    l1=len(str1)
    l2=len(str2)
    cnt=0
    for c in str1:
        if c in str2:
            cnt+=1
    cnt=cnt/min(l1,l2)
    return cnt

def match_max_pooling(str1,list2):
    ansl=[]
    for str2 in list2:
        ansl.append(match(str1,str2))
    if(len(ansl)==0):
        return 0
    return max(ansl)
