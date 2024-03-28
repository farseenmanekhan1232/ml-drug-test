import joblib
import pandas as pd
from pyopenms import MSExperiment, MzMLFile


def mz_to_molecular_mass(m_z, z):
    m_H = 1.007825
    M = m_z * z - (z * m_H)
    return M


def process_mzml_file(file_path):
    # Load and process .mzML file to extract m/z and charge values
    exp = MSExperiment()
    MzMLFile().load(file_path, exp)
    mz_values, charges = [], []
    for spectrum in exp.getSpectra():
        for mz, intensity in spectrum.get_peaks():
            mz_values.append(mz)
            charges.append(spectrum.getPrecursors()[0].getCharge())
    return mz_values, charges


def predict_substance(mz, charge):
    molecular_mass = mz_to_molecular_mass(mz, charge)
    # Load model
    model = load_model()
    # Assuming the model expects a DataFrame
    df = pd.DataFrame({"molecular_mass": [molecular_mass]})
    prediction = model.predict(df)
    return prediction[0]


def load_model():
    model_path = "./models/model.pkl"
    model = joblib.load(model_path)
    return model
