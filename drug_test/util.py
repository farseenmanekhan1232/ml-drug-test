import os
from pyopenms import MSExperiment, MzMLFile
import numpy as np
import joblib


def mz_to_molecular_mass(m_z, z):
    """
    Convert m/z value to molecular mass.
    """
    m_H = 1.007825
    M = m_z * z - (z * m_H)
    return M


def load_model(model_path):
    """
    Load the prediction model from the specified path.
    """
    model = joblib.load(model_path)
    return model


def predict_mass(model, molecular_mass):
    """
    Make a prediction based on molecular mass using the provided model.
    """
    # Assuming the model expects a single feature in 2D array
    prediction = model.predict([[molecular_mass]])
    return prediction


def process_mzml_file(file_path, model_path):
    """
    Process an .mzML file to extract m/z values, convert them to molecular mass,
    and make a prediction using a pre-trained model.
    """
    # Load the model
    model = load_model(model_path)

    # Load .mzML file
    exp = MSExperiment()
    MzMLFile().load(file_path, exp)

    # Accumulators for m/z and charge values
    mz_values = []
    charges = []

    # Iterate through all spectra
    for spectrum in exp.getSpectra():
        for mz, intensity in zip(spectrum.get_peaks()[0], spectrum.get_peaks()[1]):
            mz_values.append(mz)
            # This example assumes charge +1 for simplicity; real applications should extract actual charge state
            charges.append(1)

    # Convert lists to arrays for vectorized operations
    mz_values = np.array(mz_values)
    charges = np.array(charges)

    # Compute molecular mass for each m/z value
    molecular_masses = mz_to_molecular_mass(mz_values, charges)

    # Compute average molecular mass for simplicity
    avg_molecular_mass = np.mean(molecular_masses)

    # Predict using the molecular mass
    prediction = predict_mass(model, avg_molecular_mass)

    return prediction
