import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline

texts = [
    "I love this product", "Absolutely fantastic experience", "Best purchase ever",
    "Really happy with this", "Great quality, highly recommend", "Wonderful service",
    "Amazing, would buy again", "Exceeded my expectations", "Five stars all the way",
    "This is terrible", "Worst experience of my life", "Complete waste of money",
    "Very disappointed", "Broken on arrival", "Never buying this again",
    "Horrible quality", "Absolutely dreadful", "Do not recommend at all",
]
labels = [1,1,1,1,1,1,1,1,1, 0,0,0,0,0,0,0,0,0]

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression()),
])

pipeline.fit(texts, labels)

with open("model/sentiment_model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("Model saved to model/sentiment_model.pkl")
