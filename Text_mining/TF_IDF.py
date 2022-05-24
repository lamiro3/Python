from tkinter.tix import Tree
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.metrics.pairwise import cosine_similarity

PATH_list = [
    (
        'Text_mining\csv\땡큐서울이비인후과의원_네이버_마이플레이스_리뷰_수집.csv',
        'Text_mining\csv\땡큐서울이비인후과의원_카카오맵_리뷰_수집.csv'
    )
]

class TF_IDF:
    def __init__(self, PATH, subset):
        self.vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1,1))
        self.PATH = PATH
        self.subset = subset
        
    def getDF(self):
        return pd.read_csv(self.PATH)
    
    def getFeatures(self):
        df = self.getDF()
        df.drop_duplicates(subset=self.subset, keep='first', inplace=True)
        df.reset_index(drop = True, inplace = True)
        features = self.vectorizer.fit_transform(df[self.subset])
        return features

    def getFeatureNames(self):
        feature_names = self.vectorizer.get_feature_names()
        return feature_names
    
    def generateDTM(self):
        dtm_np = np.array(self.getFeatures().todense())
        return dtm_np
    
path = 'Text_mining\csv\땡큐서울이비인후과의원_네이버_마이플레이스_리뷰_수집.csv'

n_tf_idf = TF_IDF(path, '댓글')

# 반드시 아래 순서대로 실행되어야 함
dtm = n_tf_idf.generateDTM()
length = len(n_tf_idf.getFeatureNames())
df = n_tf_idf.getDF()

# print(pd.DataFrame(data=n_tf_idf.generateDTM(), columns=n_tf_idf.getFeatureNames())
indices = pd.Series(df.index, index=df['댓글'])
cosine_sim = cosine_similarity(dtm, dtm)
top_rated_reviews = set([])

def get_recommendations(review, cosine_sim=cosine_sim):
    idx = indices[review]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1]
    return df['댓글'].iloc[sim_scores]
 
for review in np.array(df['댓글']):
    print(get_recommendations(review))
    
print(top_rated_reviews)