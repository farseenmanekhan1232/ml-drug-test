import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import joblib

# Load the dataset
dataset_path = "./dataset.xlsx"  # Update this path
data = pd.read_excel(dataset_path)

# Feature selection
X = data[["Mass", "M+proton"]]  # Input features
y = data["Compound Name"]  # Target variable

# Splitting the dataset into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# Initialize and train the Random Forest model
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Make predictions on the test set
y_pred = model.predict(X_test)

# Evaluate the model
accuracy = accuracy_score(y_test, y_pred)
print(f"Model accuracy: {accuracy}")

# Save the model to a file
model_filename = "molecular_prediction_model.pkl"
joblib.dump(model, model_filename)
print(f"Model saved to {model_filename}")