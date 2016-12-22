import pickle
pkl_file = open('pkl/query_train.pkl', 'rb')
query = pickle.load(pkl_file)
pkl_file.close()
pkl_file = open('pkl/input_train.pkl', 'rb')
story = pickle.load(pkl_file)
pkl_file.close()
pkl_file = open('pkl/answer_train.pkl', 'rb')
answer = pickle.load(pkl_file)
pkl_file.close()
valid=pickle.load(open('pkl/valid.pkl','rb'))
stopwords=pickle.load(open('pkl/stopwords.pkl','rb'))

