import joblib


def load_model():
    # Path to your model file
    model_path = "./models/model.pkl"
    model = joblib.load(model_path)
    return model