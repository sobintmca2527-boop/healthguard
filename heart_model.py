import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
import pickle

# Load dataset
data = pd.read_csv("heart.csv")

# Check column names (important)
print(data.columns)

# Separate input and output
X = data.drop("target", axis=1)
y = data["target"]

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

# Create model
model = RandomForestClassifier()

# Train model
model.fit(X_train, y_train)

# Save model
pickle.dump(model, open("heart_model.pkl", "wb"))

print("Heart model trained successfully!")
