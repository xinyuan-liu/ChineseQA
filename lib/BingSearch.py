# -*- coding：utf-8 -*-
import requests
import lxml.html
import sys
from jieba.analyse import ChineseAnalyzer
import re,urllib.parse,urllib.request,urllib.error
from bs4 import BeautifulSoup as BS
import csv
import time,random
analyzer = ChineseAnalyzer()

def check_contain_chinese(check_str):
    for ch in check_str:
        if u'\u4e00' <= ch <= u'\u9fff':
            return True
    return False

def getKey(item):
    return item[0]

def get_story(query):
    query = query.replace("什么", " ").replace("的", " ").replace("是", " ").replace("几", " ").replace("多少", " ").replace("哪个", " ").replace("哪所", " ").replace("谁", " ").replace("哪一", " ").replace("哪里", " ").replace("?", "")
    flag=True
    while flag:
        try:
            r = requests.get('https://cn.bing.com/search?q='+query)
            flag=False
        except:
            pass
    tree = BS(r.text, "lxml")
    answer = ''
    for node in tree.findAll(attrs={'class': re.compile(r"b_algo")}):
        try:
            r = requests.get(node.h2.a['href'], verify=False, timeout=1)
            r.close()
            r.encoding =  r.apparent_encoding
            tree = BS(r.text, "lxml")
            if tree.body is None:
                continue
            aList = [str.replace('\u3000', '').strip() for str in re.split(r'[\r\n]', tree.body.text)]
            aList = [str for str in aList if len(str) > 2 and len(str) < 500 and check_contain_chinese(str)]# and str[:8] != 'function' and str[:5] != 'alert' and str[:1] != '<' and str[:6] != 'window' and str[:6] != 'window']
            aList = [[0, str] for str in aList]
            for t in analyzer(query):
                for str in aList:
                    if str[1].find(t.text) != -1:
                        str[0] += 1
            aList.sort(key=getKey, reverse=True)
            for str in aList:
                if str[0] <= 1:
                    break
                answer += str[1]
                if len(answer) > 300:
                    break
            answer += '\n'
        except requests.exceptions.Timeout:
            pass
        if len(answer) > 1000:
            break
    return answer

def get_story_1(word):
    baseUrl = 'http://cn.bing.com/search?'
    word = word.encode(encoding='utf-8', errors='strict')
    data = {'q':word}
    data = urllib.parse.urlencode(data)
    url = baseUrl+data
    try:
        html = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print(e.code)
    except urllib.error.URLError as e:
        print(e.reason)
    soup = BS(html,"html.parser")
    td = soup.findAll("h2")
    count = soup.findAll(class_="sb_count")
    res='';
    i=0
    for t in td:
        res+=(t.get_text())+'\n'
        i+=1
        if(i==9):
            break
    i=0
    td=soup.findAll('p')
    for t in td:
        res+=(t.get_text())+'\n'
        i+=1
        if(i==9):
            break
    return res.replace('...',' ')

def get_story_2(word):
    word = word.encode(encoding='utf-8', errors='strict')
    baseUrl = 'http://www.baidu.com/s'
    page = 1 #第几页

    data = {'wd':word,'pn':str(page-1)+'0','tn':'baidurt','ie':'utf-8','bsst':'1'}
    data = urllib.parse.urlencode(data)
    url = baseUrl+'?'+data

    try:
        html = urllib.request.urlopen(url)
    except urllib.error.HTTPError as e:
        print(e.code)
    except urllib.error.URLError as e:
        print(e.reason)
    soup = BS(html,"html.parser")
    td = soup.find_all(class_='f')
    res='';
    for t in td:
        res+= (t.h3.a.get_text())+'\n'
        #print (t.h3.a['href'])

        font_str = t.find_all('font',attrs={'size':'-1'})[0].get_text()
        start = 0 #起始
        realtime = t.find_all('div',attrs={'class':'realtime'})
        if realtime:
            realtime_str = realtime[0].get_text()
            start = len(realtime_str)
            #print (realtime_str)
        end = font_str.find('...')
        res+= (font_str[start:end]+'\n')
    return res.replace('...',' ')


