import lib.HeadWord
import lib.BingSearch
import lib.word2vec
import lib.ClassPredictor
import lib.SimpleMatch
import lib.KGraph
import lib.Data as data
import jieba
import jieba.analyse
import jieba.posseg
from sklearn.externals import joblib

print('READY')

def get_alternative_words(query,story,classes):
    word_list=list(jieba.posseg.cut(story))
    ansset=set()
    for pair in word_list:
        if query.find(pair.word)==-1:#ignore words already in question
            if not pair.word in data.stopwords:
                if pair.flag[0] in classes:
                    if pair.word.strip()!='':
                        ansset.add(pair.word)
    return list(ansset)

def process_query(query):
    query_words=list(jieba.cut(query))
    headwords=lib.HeadWord.get_head_word(query)
    #print(headwords)
    story=lib.BingSearch.get_story_2(query)
    #print(story)
    classes=lib.ClassPredictor.predict(query,lib.word2vec.vector)
    word_list=list(jieba.cut(story))
    possible_answer=get_alternative_words(query,story,classes)
    word_freq=lib.SimpleMatch.get_word_frequency(possible_answer,word_list)
    #TODO merge similar words
    length=len(possible_answer)
    tags_l=lib.KGraph.get_tags_concurrent(possible_answer)
    ans_feature_list=[]
    X=[]

    for i in range(length):
        freq=word_freq[i] # 1 ~ n
        tags=tags_l[i]
        #print(tags)
        tag_match=lib.word2vec.get_sim_max_pooling(headwords,tags) # -1 ~ 1
        headword_match=lib.SimpleMatch.match_max_pooling(possible_answer[i],headwords) # 0 ~ 1
        question_match_max_pooling=lib.word2vec.get_sim_max_pooling(possible_answer[i],query_words) # -1 ~ 1
        question_match_mean_pooling=lib.word2vec.get_sim_mean_pooling(possible_answer[i],query_words) #-1 ~ 1
        match_vec=lib.SimpleMatch.get_match_vec(possible_answer[i],query,word_list)#TODO 根据问题中词在story中词频计算权重
        match_sum=0 # 0 ~ freq*2*window_size
        for num in match_vec:
            match_sum+=num
        x=[freq, tag_match, headword_match, question_match_max_pooling, question_match_mean_pooling]
        x.extend(match_vec)
        X.append(x)
        ans_feature_list.append((i,0,freq, tag_match, headword_match, question_match_max_pooling, question_match_mean_pooling, match_sum))

    maxfreq=max(ans_feature_list,key=lambda t:t[2])[2]
    maxmatchsum=max(ans_feature_list,key=lambda t:t[7])[7]
    ans_weight_list=[]
    for i in range(length):
        weight=0.5*ans_feature_list[i][2]/maxfreq+3*ans_feature_list[i][3]+2*ans_feature_list[i][4]+ans_feature_list[i][5]+2*ans_feature_list[i][6]+2*ans_feature_list[i][7]/maxmatchsum  #naive model, maybe we need a complex one
        ans_weight_list.append((i,weight))
    
    ans_weight_list=sorted(ans_weight_list,key=lambda t:t[1])
    ans_weight_list.reverse()
    print('Naive')
    for i in range(min(5,len(possible_answer))):
        print(possible_answer[ans_weight_list[i][0]])

    print('RandomForest')
    clf=joblib.load('models/rf.model')
    Y=clf.predict_proba(X)
    ans_pre_list=[]
    #print(Y)
    for i in range(len(Y)):
        ans_pre_list.append((i,Y[i][1]))
    ans_pre_list=sorted(ans_pre_list,key=lambda t:t[1])
    ans_pre_list.reverse()
    for i in range(min(5,len(possible_answer))):
        print(possible_answer[ans_pre_list[i][0]])
    lib.KGraph.store_cache_file()

def cache_query(query):
    query_words=list(jieba.cut(query))

    story=lib.BingSearch.get_story_1(query)
    classes=lib.ClassPredictor.predict(query,lib.word2vec.vector)

    possible_answer=get_alternative_words(query,story,classes)

    #TODO merge similar words
    length=len(possible_answer)
    for i in range(length):
        tags=lib.KGraph.get_tags(possible_answer[i])
    lib.KGraph.store_cache_file()

if __name__ == "__main__":
    for i in data.valid:
        query=input()
        #print(query)
        process_query(query)
