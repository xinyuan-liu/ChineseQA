#!/usr/local/bin/python3
from __future__ import print_function
import pickle
import jieba
import requests
import json
import queue
import threading
KGNameCache=pickle.load(open('./pkl/KGNameCache.pkl','rb'))
KGTagCache=pickle.load(open('./pkl/KGTagCache.pkl','rb'))
def KG_query_name(name):
    global mutex3
    if name in KGNameCache:
        data=KGNameCache[name]
    else:
        r=requests.get('http://139.224.229.201:30001/?p='+name)
        mutex3.acquire()
        KGNameCache[name]=r.text
        mutex3.release()
        data=r.text
    try:
        data=json.loads(data)
    except:
        data=[]
    return data

def KG_query_tags(entity):
    global mutex4
    if entity in KGTagCache:
        data=KGTagCache[entity]
    else:
        r=requests.get('https://crl.ptopenlab.com:8800/cndbpedia/api/entityTag?entity='+entity)
        mutex4.acquire()
        KGTagCache[entity]=r.text
        mutex4.release()
        data=r.text
    data=json.loads(data)
    return data['Tags']

def KG_query(str):
    entities=KG_query_name(str)
    print(entities)
    for entity in entities:
        data=KG_query_tags(entity)
        print(data)

def get_tags(str):
    l=KG_query_name(str)
    lt=set()
    for e in l:
        t=KG_query_tags(e)
        for a in t:
            if a=='None':
                continue
            ws=list(jieba.cut(a))
            for b in ws:
                lt.add(b)
    return list(lt)

def mythread():
    global mutex1,q,word_l,res,mutex2
    job=-1
    while(True):
        mutex1.acquire()
        if q.empty():
            job=None
        else:
            job=q.get()
        mutex1.release()
        if job==None:
            return
        tags=get_tags(word_l[job])
        mutex2.acquire()
        res[job]=tags
        mutex2.release()

def get_tags_concurrent(words,num=32):
    global mutex1,q,word_l,res,mutex2,mutex3,mutex4
    word_l=words
    l=len(words)
    res=[0] * l
    q=queue.Queue()
    for i in range(l):
        q.put(i)
    mutex1=threading.Lock()
    mutex2=threading.Lock()
    mutex3=threading.Lock()
    mutex4=threading.Lock()
    threads=[]
    for i in range(num):
        threads.append(threading.Thread(target=mythread))
    for t in threads:
        t.start()
    for t in threads:
        t.join()
    return res

def store_cache_file():
    pickle.dump(KGTagCache,open('./pkl/KGTagCache.pkl','wb'))
    pickle.dump(KGNameCache,open('./pkl/KGNameCache.pkl','wb'))



