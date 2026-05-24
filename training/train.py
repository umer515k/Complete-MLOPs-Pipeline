import pickle
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.datasets import load_files
from sklearn.model_selection import train_test_split
from sklearn import metrics

# Simple labeled dataset — no downloads needed
texts = [
    "I love this product", "Absolutely fantastic experience", "Best purchase ever",
    "Really happy with this", "Great quality, highly recommend", "Wonderful service",
    "This is terrible", "Worst experience of my life", "Complete waste of money",
    "Very disappointed", "Broken on arrival", "Never buying this again",
    "Not bad, could be better", "It's okay I guess", "Average product",
]
labels = [1,1,1,1,1,1, 0,0,0,0,0,0, 0,0,0]  # 1=positive, 0=negative

X_train, X_test, y_train, y_test = train_test_split(
    texts, labels, test_size=0.2, random_state=42
)

pipeline = Pipeline([
    ("tfidf", TfidfVectorizer()),
    ("clf", LogisticRegression()),
])

pipeline.fit(X_train, y_train)
preds = pipeline.predict(X_test)
print(f"Accuracy: {metrics.accuracy_score(y_test, preds):.2f}")

# Save model
with open("model/sentiment_model.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("Model saved to model/sentiment_model.pkl")
