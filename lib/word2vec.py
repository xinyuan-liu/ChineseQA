import pickle
import numpy as np

vector=pickle.load(open('pkl/gensim_vector.pkl','rb'))

def get_vector(word):
    if word in vector:
        return vector[word]
    return None

def cosine(a,b):
    return a.dot(b)/(np.linalg.norm(a)*np.linalg.norm(b))

def get_sim(a,b):
    a=get_vector(a)
    if a == None:
        return 0.0#TODO: 未登录词
    a=np.array(a)
    b=get_vector(b)
    if b == None:
        return 0.0
    b=np.array(b)
    return cosine(a,b)

def get_sim_max_pooling(a,l):
    ansl=[]
    if (not isinstance(a,str)) and isinstance(a,list):
        for c in a:
            for b in l:
                ansl.append(get_sim(b,c))
    else:
        for b in l:
            ansl.append(get_sim(a,b))
    if len(ansl)==0:
        return 0;
    return max(ansl)


def get_sim_mean_pooling(a,l):
    ansl=[]
    for b in l:
        ansl.append(get_sim(a,b))
    if len(ansl)==0:
        return 0
    return sum(ansl)/len(ansl)
