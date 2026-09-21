# app/ml/feature_builder.py

import numpy as np
from app.ml.fft_feature_extractor import extract_fft_features
from app.ml.data_preprocessor import preprocess_dataset

def build_features_from_signals(signals, fft_bins=256):
    """
    Converts raw signals into fully processed feature vectors
    ready for 100-virus model training.

    Steps:
        1. FFT extraction
        2. Preprocessing (normalize + clip outliers)

    Parameters:
        signals (list or np.ndarray): Raw sensor signals
        fft_bins (int): Number of FFT bins to keep

    Returns:
        np.ndarray: Final feature matrix
    """

    # Step 1 — FFT feature extraction
    fft_matrix = []
    for sig in signals:
        fft_vec = extract_fft_features(sig, max_features=fft_bins)
        fft_matrix.append(fft_vec)

    fft_matrix = np.array(fft_matrix)

    # Step 2 — Preprocessing pipeline
    processed = preprocess_dataset(fft_matrix)

    return processed
