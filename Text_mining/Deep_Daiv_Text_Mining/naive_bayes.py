from sklearn.metrics import accuracy_score
from sklearn.naive_bayes import MultinomialNB
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import pandas as pd
import re

class TF_IDF:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(min_df=1, ngram_range=(1,1))

    def getFeatures(self, df):
        df.reset_index(drop = True, inplace = True)
        features = self.vectorizer.fit_transform(df)
        return features

    def getFeatureNames(self):
        feature_names = self.vectorizer.get_feature_names()
        return feature_names
    
    def generateDTM(self, df):
        dtm_np = np.array(self.getFeatures(df).todense())
        return dtm_np

# 반드시 아래 순서대로 실행되어야 함
TFID = TF_IDF()
df = pd.read_csv('Text_mining\csv\kakao_review.csv')
df = df.dropna()
df.drop_duplicates(subset='댓글', keep='first', inplace=True)
df['댓글'] = df['댓글'].map(lambda x: re.sub(r'[^\w\s]', ' ', x))

length = len(df)

train, test = df[:length//2], df[length//2:]

train['평점'] = train['평점'].astype(str)
test['평점'] = test['평점'].astype(str)

train_dtm = {
    "review": TFID.generateDTM(train['댓글']),
    "score": train['평점']
}

test_dtm = {
    "review": TFID.generateDTM(test['댓글']),
    "score": test['평점']
}

mod = MultinomialNB(alpha=1.0, class_prior=None, fit_prior=None) # 라플라스 스무딩 적용
mod.fit(train_dtm["review"], train_dtm["score"])

predicted = mod.predict(test_dtm["review"])
print('Accuracy Rate: ', accuracy_score(test_dtm["score"], predicted))