import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV
import pickle

df = pd.read_csv("lemmatized.csv")

vectorizer = TfidfVectorizer(max_features=10000, ngram_range=(1,2))
tfidf = vectorizer.fit_transform(df['content'].fillna(''))

model = LogisticRegression(max_iter=2000, solver='saga', C = 0.1, n_jobs = -1)
model.fit(tfidf, df['category'])

f = open('logregModel.pkl', 'wb')
pickle.dump(model, f)
f.close()

f = open('vectorizer.pkl', 'wb')
pickle.dump(vectorizer, f)
f.close() 