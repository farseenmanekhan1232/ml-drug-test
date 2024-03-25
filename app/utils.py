import os
from pyopenms import MSExperiment, MzMLFile


def handle_mzml_upload(file_storage):
    """
    Handle the upload of a .mzML file, extracting m/z values and charges.

    Parameters:
    - file_storage: The FileStorage object containing the uploaded file.

    Returns:
    - A tuple of two lists: (mz_values, charges) extracted from the file.
    """
    filename = os.path.join("uploads", file_storage.filename)
    file_storage.save(filename)

    # Load the .mzML file
    exp = MSExperiment()
    MzMLFile().load(filename, exp)

    # Extract m/z values and charges
    mz_values = []
    charges = []
    for spectrum in exp:
        for mz, intensity in spectrum.get_peaks():
            mz_values.append(mz)
            charges.append(
                spectrum.getPrecursors()[0].getCharge()
                if spectrum.getPrecursors()
                else 1
            )  # Default charge 1

    return mz_values, charges


def mz_to_molecular_mass(m_z, z):
    """
    Convert m/z value to molecular mass.

    Parameters:
    - m_z: The m/z value (mass-to-charge ratio).
    - z: The charge of the ion.

    Returns:
    - The molecular mass of the compound.
    """
    m_H = 1.007825
    M = m_z * z - (z * m_H)
    return M
