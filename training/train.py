import mlflow
import mlflow.sklearn
import pickle
import os
from datasets import load_dataset
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.svm import LinearSVC
from sklearn.pipeline import Pipeline
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# Load real IMDB dataset
print("Loading IMDB dataset...")
dataset = load_dataset("stanfordnlp/imdb")

train_texts = dataset["train"]["text"]
train_labels = dataset["train"]["label"]
test_texts = dataset["test"]["text"]
test_labels = dataset["test"]["label"]

print(f"Training samples: {len(train_texts)}")
print(f"Test samples: {len(test_texts)}")

# Models to compare
models = {
    "logistic_regression": LogisticRegression(max_iter=1000),
    "naive_bayes": MultinomialNB(),
    "linear_svm": LinearSVC(max_iter=1000),
}

mlflow.set_experiment("sentiment-analysis")

best_f1 = 0
best_model = None
best_model_name = ""

for model_name, classifier in models.items():
    print(f"\nTraining {model_name}...")

    with mlflow.start_run(run_name=model_name):
        pipeline = Pipeline([
            ("tfidf", TfidfVectorizer(max_features=10000, ngram_range=(1, 2))),
            ("clf", classifier),
        ])

        pipeline.fit(train_texts, train_labels)
        predictions = pipeline.predict(test_texts)

        # Metrics
        accuracy  = accuracy_score(test_labels, predictions)
        precision = precision_score(test_labels, predictions)
        recall    = recall_score(test_labels, predictions)
        f1        = f1_score(test_labels, predictions)

        print(f"  Accuracy:  {accuracy:.4f}")
        print(f"  Precision: {precision:.4f}")
        print(f"  Recall:    {recall:.4f}")
        print(f"  F1:        {f1:.4f}")

        # Log to MLflow
        mlflow.log_param("model_type", model_name)
        mlflow.log_param("max_features", 10000)
        mlflow.log_param("ngram_range", "(1,2)")
        mlflow.log_metric("accuracy", accuracy)
        mlflow.log_metric("precision", precision)
        mlflow.log_metric("recall", recall)
        mlflow.log_metric("f1", f1)
        mlflow.sklearn.log_model(pipeline, "model")

        if f1 > best_f1:
            best_f1 = f1
            best_model = pipeline
            best_model_name = model_name

print(f"\nBest model: {best_model_name} (F1: {best_f1:.4f})")

# Save best model
os.makedirs("model", exist_ok=True)
with open("model/sentiment_model.pkl", "wb") as f:
    pickle.dump(best_model, f)

print("Best model saved to model/sentiment_model.pkl")
