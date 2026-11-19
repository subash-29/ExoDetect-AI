import pickle
import joblib
from pathlib import Path
import streamlit as st


# Project directory
PROJECT_ROOT = Path(__file__).resolve().parents[2]

# Model artifact path
MODEL_PATH = (
    PROJECT_ROOT
    / "models"
    / "exodetect_prediction_pipeline.pkl"
)


@st.cache_resource
def load_prediction_model():

    if not MODEL_PATH.exists():
        raise FileNotFoundError(
            f"Model artifact not found: {MODEL_PATH}"
        )

    try:
        artifact = joblib.load(MODEL_PATH)

    except Exception:
        with open(MODEL_PATH, "rb") as file:
            artifact = pickle.load(file)

    return artifact


def get_model_information(artifact):

    return {
        "model_name": artifact["model_name"],
        "number_of_features": artifact["number_of_features"],
        "target_classes": artifact["target_classes"],
        "feature_names": artifact["feature_names"]
    }