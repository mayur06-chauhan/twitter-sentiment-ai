import sklearn
print("Training with sklearn version:", sklearn.__version__)

import pandas as pd
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression

# Load dataset
df = pd.read_csv("training.1600000.processed.noemoticon.csv",
                 encoding="latin-1",
                 header=None)

df = df[[0, 5]]
df.columns = ["sentiment", "text"]

# Convert labels
df["sentiment"] = df["sentiment"].replace(4, 1)

# Use smaller sample (fast training)
df = df.sample(50000)

# Vectorization
vectorizer = TfidfVectorizer(max_features=5000)
X = vectorizer.fit_transform(df["text"])
y = df["sentiment"]

# Train model
model = LogisticRegression()
model.fit(X, y)

# Save artifacts
joblib.dump(model, "model/sentiment_model.pkl")
joblib.dump(vectorizer, "model/vectorizer.pkl")

print("Model saved!")

