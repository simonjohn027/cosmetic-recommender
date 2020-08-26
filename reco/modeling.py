import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import joblib

dataset = pd.read_csv('datasets\cosmetics.csv')

tfidf = TfidfVectorizer(stop_words='english')

dataset['Ingredients'] = dataset['Ingredients'].fillna('')
tfidf_matrix = tfidf.fit_transform(dataset['Ingredients'])

cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
print(tfidf_matrix.shape)

joblib.dump(cosine_sim, 'model.file', compress = 1)