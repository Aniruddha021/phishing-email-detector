import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import joblib

# Load data
data = pd.read_csv("phishing_email.csv")

X = data["text"]
y = data["label"]

# Convert text to numbers
vectorizer = TfidfVectorizer()

X_vector = vectorizer.fit_transform(X)

# Train model
model = LogisticRegression()
model.fit(X_vector, y)

# Save files
joblib.dump(model, "phishing_model.pkl")
joblib.dump(vectorizer, "vectorizer.pkl")

print("Model trained successfully!")
