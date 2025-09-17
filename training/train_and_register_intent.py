import mlflow
import mlflow.sklearn
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
import pandas as pd
import os

# Load dataset
df = pd.read_csv("intent_data.csv")

X = df["text"]
y = df["intent"]

# Build pipeline
pipeline = Pipeline([
    ("tfidf", TfidfVectorizer(ngram_range=(1,2), min_df=1)),
    ("clf", LogisticRegression(max_iter=500))
])

pipeline.fit(X, y)

# Evaluate
acc = pipeline.score(X, y)
print(f"Training Accuracy: {acc:.2f}")

# MLflow setup
mlflow.set_tracking_uri(os.getenv("MLFLOW_TRACKING_URI", "http://mlflow:5000"))
MODEL_NAME = os.getenv("MLFLOW_MODEL_NAME", "customer_intent_classifier")

with mlflow.start_run() as run:
    mlflow.log_metric("train_accuracy", acc)
    mlflow.sklearn.log_model(
        sk_model=pipeline,
        artifact_path="model",
        registered_model_name=MODEL_NAME
    )
