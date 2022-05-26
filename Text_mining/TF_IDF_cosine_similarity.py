from tkinter.tix import Tree
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
from sklearn.metrics.pairwise import cosine_similarity

PATH_list = [
    (
        'Text_mining\csv\땡큐서울이비인후과의원_네이버_마이플레이스_리뷰_수집.csv',
        'Text_mining\csv\땡큐서울이비인후과의원_카카오맵_리뷰_수집.csv'
    )
]

class TF_IDF:
    def __init__(self, subset):
        self.vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1,1))
        self.subset = subset
    
    def getFeatures(self, df):
        df.drop_duplicates(subset=self.subset, keep='first', inplace=True)
        df.reset_index(drop = True, inplace = True)
        features = self.vectorizer.fit_transform(df[self.subset])
        return features

    def getFeatureNames(self):
        feature_names = self.vectorizer.get_feature_names()
        return feature_names
    
    def generateDTM(self, df):
        dtm_np = np.array(self.getFeatures(df).todense())
        return dtm_np
    
path = 'Text_mining\csv\땡큐서울이비인후과의원_네이버_마이플레이스_리뷰_수집.csv'

n_tf_idf = TF_IDF('댓글')

# 반드시 아래 순서대로 실행되어야 함
df = pd.read_csv(path)
dtm = n_tf_idf.generateDTM(df)
length = len(n_tf_idf.getFeatureNames())

# print(pd.DataFrame(data=n_tf_idf.generateDTM(), columns=n_tf_idf.getFeatureNames())
indices = pd.Series(df.index, index=df['댓글'])
cosine_sim = cosine_similarity(dtm, dtm)
top_related_reviews = []

def get_recommendations(review, cosine_sim=cosine_sim):
    idx = indices[review]
    sim_scores = list(enumerate(cosine_sim[idx])) # [(단어 인덱스 번호, 코사인 유사도)]꼴의 리스트
    sim_scores.sort(key=lambda x: x[1], reverse=True)
    review_indices = list(map(lambda x:x[0], sim_scores))[1] # 자기 자신 제외 가장 비슷한 리뷰 출력
    return df['댓글'].iloc[review_indices]

for review in np.array(df['댓글']):
    top_related_reviews.append(get_recommendations(review))

print(top_related_reviews)

# 유사도 검사를 통해 가장 유사한 것 끼리 묶어서 워드클라우드 형태로 출력하기