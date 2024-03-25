def process_mzml_file(file):

    m_z = extract_mz_value(file)
    molecular_mass = mz_to_molecular_mass(m_z, charge)
    return molecular_mass


def make_prediction(molecular_mass):
    model = load_model()

    prediction_input = [[molecular_mass]]
    prediction = model.predict(prediction_input)
    return prediction


def mz_to_molecular_mass(m_z, z=1):
    m_H = 1.007825
    M = m_z * z - (z * m_H)
    return M
