import pandas as pd
import os
import joblib
import logging
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report
from sklearn.preprocessing import LabelEncoder


logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


def load_data(filepath):
    """
    Load dataset from the specified filepath.

    :param filepath: Path to the dataset file.
    :return: DataFrame containing the dataset.
    """
    try:
        df = pd.read_excel(filepath)
        df = df[["Formula", "Compound Name", "Mass", "M+proton"]]
        return df
    except Exception as e:
        logging.error(f"Failed to load data from {filepath}: {e}")
        raise


def preprocess_data(df):
    """
    Preprocess the dataset: encode categorical variables and split into training and test sets.

    :param df: DataFrame containing the dataset.
    :return: Tuple of train-test split of features and target variable.
    """
    logging.info("Processing training data...")
    le = LabelEncoder()
    df["Compound Name"] = le.fit_transform(df["Compound Name"])
    X = df[["Mass", "M+proton"]]
    y = df["Compound Name"]
    return train_test_split(X, y, test_size=0.2, random_state=42)


def train_model(X_train, y_train, output_path="drug_test/drug_prediction_model.pkl"):
    """
    Train a RandomForestClassifier on the training data and save the model.

    :param X_train: Training features.
    :param y_train: Training target variable.
    :param output_path: Path to save the trained model.
    :return: Trained model.
    """
    logging.info("Training model...")
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    joblib.dump(model, output_path)
    return model


def main(filepath, model_output_path="drug_test/drug_prediction_model.pkl"):
    """
    Main function to execute the model training pipeline.

    :param filepath: Path to the dataset file.
    :param model_output_path: Path to save the trained model.
    """
    logging.info("Loading training data...")
    df = load_data(filepath)
    X_train, X_test, y_train, y_test = preprocess_data(df)
    model = train_model(X_train, y_train, model_output_path)
    predictions = model.predict(X_test)
    logging.info("\n" + classification_report(y_test, predictions))


filepath = os.path.join(os.getcwd(), "drug_test", "data", "dataset.xlsx")
model_output_path = os.path.join(os.getcwd(), "drug_test", "drug_prediction_model.pkl")
main(filepath, model_output_path)
