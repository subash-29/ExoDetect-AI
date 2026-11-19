import sys
from pathlib import Path

import streamlit as st

# Add project root to Python path
PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils.model_loader import (
    load_prediction_model,
    get_model_information
)
from app.utils.theme import apply_theme, metric_card, feature_card

# Page configuration
st.set_page_config(
    page_title="ExoDetect AI",
    page_icon="🪐",
    layout="wide",
    initial_sidebar_state="expanded"
)

apply_theme()


# Load model
try:
    artifact = load_prediction_model()
    model_info = get_model_information(artifact)
    model_status = "ONLINE"
except Exception as error:
    artifact = None
    model_info = None
    model_status = "ERROR"
    st.error(f"Model loading failed: {error}")


# Sidebar
with st.sidebar:
    st.title("🪐 ExoDetect AI")
    st.caption("NASA Exoplanet Detection System")

    st.divider()

    st.markdown("### Navigation")
    st.page_link("app.py", label="Dashboard", icon="🏠")

    st.divider()

    st.markdown("### System Status")

    if model_status == "ONLINE":
        st.success("Prediction Model Online")
    else:
        st.error("Prediction Model Offline")

    st.caption("Powered by CatBoost Machine Learning")


# Main dashboard
st.markdown("""
<div class="hero">
<span class="hero-tag">NASA Exoplanet Detection System</span>
<h1>🪐 ExoDetect AI</h1>
<p>
An intelligent exoplanet classification system using
NASA Kepler mission catalogue data and machine learning.
</p>
<div class="chip-row">
<span class="chip">🔭 Kepler</span>
<span class="chip">🛰️ TESS Validation</span>
<span class="chip">🌲 CatBoost</span>
<span class="chip">🔍 SHAP</span>
</div>
</div>
""", unsafe_allow_html=True)


st.markdown("## Mission Overview")

st.write(
    "ExoDetect AI analyzes astronomical catalogue parameters "
    "to classify potential exoplanet observations into three categories: "
    "Candidate, Confirmed, and False Positive."
)

# Metrics
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        metric_card("🔭", "9,564", "Kepler Observations"),
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        metric_card("🧬", "31", "Model Features"),
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        metric_card("🏷️", "3", "Classification Classes"),
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        metric_card("🎯", "75.27%", "Test Macro F1 Score"),
        unsafe_allow_html=True
    )


st.markdown("---")

st.markdown("## Machine Learning Model")

if model_info:

    col1, col2 = st.columns(2)

    with col1:
        st.markdown(
            '<div class="info-card">'
            '<h4>Model Information</h4>'
            f'<div class="kv-row"><span class="kv-key">Model</span>'
            f'<span class="kv-val">{model_info["model_name"]}</span></div>'
            f'<div class="kv-row"><span class="kv-key">Features</span>'
            f'<span class="kv-val">{model_info["number_of_features"]}</span></div>'
            '<div class="kv-row"><span class="kv-key">Algorithm</span>'
            '<span class="kv-val">CatBoost Classifier</span></div>'
            '<div class="kv-row"><span class="kv-key">Preprocessing</span>'
            '<span class="kv-val">Median Imputation</span></div>'
            '</div>',
            unsafe_allow_html=True
        )

    with col2:
        pills = "".join(
            f'<span class="pill">🔹 {category}</span>'
            for category in model_info["target_classes"]
        )

        st.markdown(
            '<div class="info-card">'
            '<h4>Prediction Categories</h4>'
            f'{pills}'
            '</div>',
            unsafe_allow_html=True
        )

st.markdown("---")

st.markdown("## About This Project")

st.write(
    "ExoDetect AI is an end-to-end machine learning project built using "
    "NASA exoplanet catalogue data."
)

features = [
    ("📊", "Exploratory Data Analysis", "Understanding the structure and quality of the Kepler catalogue."),
    ("🧹", "Preprocessing & Feature Engineering", "Cleaning, imputing and preparing astronomical parameters."),
    ("🤖", "Machine Learning Classification", "CatBoost model for three-class disposition prediction."),
    ("🧠", "Deep Learning with PyTorch", "Neural network experiments for comparison."),
    ("🌌", "Cross-Mission Validation", "Testing Kepler-trained models on TESS data."),
    ("🔍", "Model Explainability", "SHAP analysis to understand model decisions."),
    ("🧪", "Feature Ablation Experiments", "Measuring the impact of removing key features."),
    ("🚀", "Prediction Pipeline", "Interactive page for real-time classification."),
]

for row_start in range(0, len(features), 4):
    columns = st.columns(4)
    for column, (icon, title, text) in zip(columns, features[row_start:row_start + 4]):
        with column:
            st.markdown(feature_card(icon, title, text), unsafe_allow_html=True)

st.info(
    "Note: This model uses astronomical catalogue parameters. "
    "It does not directly analyze raw telescope light curves."
)

st.caption("ExoDetect AI | NASA Exoplanet Classification Project | 2026")
