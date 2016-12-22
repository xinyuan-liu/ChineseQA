import jieba
import nltk
import os
import re
from nltk.parse.stanford import StanfordParser
os.environ['CLASSPATH']='$CLASSPATH:/Users/liuxinyuan/Desktop/WebDataMining/stanford parser/stanford-parser-full-2015-12-09'
parser=StanfordParser(model_path='/Users/liuxinyuan/Desktop/WebDataMining/stanford parser/edu/stanford/nlp/models/lexparser/chineseFactored.ser.gz')

def is_qw(word):
    pattern = re.compile(u'哪.*|谁|什么|.*几.*|.*多少.*')
    match = pattern.match(word)
    if match:
        return True
    else :
        return False

def is_vce(word):
    pattern = re.compile(u'是|叫|名叫|为|称为|作为')
    match = pattern.match(word)
    if match:
        return True
    else :
        return False

def get_parent(root,node):
    if isinstance(root,str):
        return None
    for n in reversed(root):
        if (not isinstance(n,str)) and node in n:
            return n
        res=get_parent(n,node)
        if res != None:
            return res

def get_head_word(str):
    root=list(parser.parse(list(jieba.cut(str))))
    leaves=root[0].leaves()
    #print(root[0])
    qw=''
    for w in reversed(leaves):
        if(is_qw(w)):
            qw=w
            break
    head_word=None
    if(qw!=''):
        #print(qw)
        head_word=get_head_word_right(root,qw)
    if(head_word==None):
        vce=''
        for w in reversed(leaves):
            if(is_vce(w)):
                vce=w
                break
        head_word=get_head_word_left(root,vce)
        #print(vce)
    #print(head_word)
    if head_word==None:
        head_word=[]
    if qw=='谁' or qw=='哪位' or '人' in head_word or '人物' in head_word:
        head_word.append('人')
        head_word.append('人物')
    return list(set(head_word))

def get_head_word_right(root,qw):

    parent=get_parent(root,qw)
    child=qw
    while parent!=None:#add if guard for NP
        if len(parent)!=1:
            if parent.index(child)+1==len(parent):
                break;
            if parent[len(parent)-1].label().startswith('N'):
                break;
        child=parent
        parent=get_parent(root,child)
    if parent==None:
        return
    index=parent.index(child)
    if(index+1<len(parent)):
        return(parent[len(parent)-1].leaves())
    return

def get_head_word_left(root,vce):
    parent=get_parent(root,vce)
    child=vce
    phrase=None
    while parent!=None:
        index=parent.index(child)
        flag=False
        if index!=0:
            for i in reversed(range(0,index)):
                if not (parent[i].label()=='ADVP' or parent[i].label()=='VP'  or parent[i].label()=='SB'):#or aggressively startswith('N')
                    flag=True
                    phrase=parent[i]
                    break;
            if(flag):
                break
        child=parent
        parent=get_parent(root,child)
    if parent==None:
        return;
    while not isinstance(phrase,str):
        phrase=phrase[len(phrase)-1]
    if phrase=='的':
        return []
    return [phrase]
