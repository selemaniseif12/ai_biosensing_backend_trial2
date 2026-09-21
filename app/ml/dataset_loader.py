# app/ml/dataset_loader.py

import numpy as np
import os

def load_100_virus_dataset(features_path: str, labels_path: str):
    """
    Loads the 100-virus dataset from .npy files.

    Parameters:
        features_path (str): Path to features_100.npy
        labels_path (str): Path to labels_100.npy

    Returns:
        X (np.ndarray): Feature vectors
        y (np.ndarray): Virus ID labels (1–100)
    """

    if not os.path.exists(features_path):
        raise FileNotFoundError(f"Features file not found: {features_path}")

    if not os.path.exists(labels_path):
        raise FileNotFoundError(f"Labels file not found: {labels_path}")

    X = np.load(features_path)
    y = np.load(labels_path)

    if len(X) != len(y):
        raise ValueError("Feature and label arrays must have the same length.")

    print(f"Loaded dataset: {len(X)} samples, {len(set(y))} virus classes.")

    return X, y
