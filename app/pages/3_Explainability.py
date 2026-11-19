import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils.theme import apply_theme, page_hero, show_chart, sidebar_brand

import streamlit as st
import pandas as pd
import numpy as np
import json
import plotly.express as px
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Explainability | ExoDetect AI",
    page_icon="🔍",
    layout="wide"
)

apply_theme()

sidebar_brand()


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = PROJECT_ROOT / "data" / "processed"

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

page_hero(
    "🔍",
    "Model Explainability",
    "Understand how ExoDetect AI makes predictions "
    "and which astronomical features influence its decisions.",
    "Feature Importance · SHAP · Ablation"
)

st.divider()
# --------------------------------------------------
# 1. CATBOOST FEATURE IMPORTANCE
# --------------------------------------------------

st.header("1. CatBoost Feature Importance")

st.markdown(
    """
    This chart shows which astronomical features contribute most
    to the CatBoost model's prediction process.

    Higher importance indicates greater influence on the model's
    decisions. However, importance does not imply causation.
    """
)

FEATURE_IMPORTANCE_PATH = DATA_PATH / "feature_importance.csv"


@st.cache_data
def load_feature_importance():
    return pd.read_csv(FEATURE_IMPORTANCE_PATH)


if FEATURE_IMPORTANCE_PATH.exists():

    importance_df = load_feature_importance()

    top_n = st.slider(
        "Number of features to display",
        min_value=5,
        max_value=31,
        value=15
    )

    chart_df = importance_df.head(top_n).sort_values(
        "importance",
        ascending=True
    )

    fig = px.bar(
        chart_df,
        x="importance",
        y="feature",
        orientation="h",
        title=f"Top {top_n} Features Influencing CatBoost",
        labels={
            "importance": "Feature Importance",
            "feature": "Astronomical Feature"
        },
        template="plotly_dark"
    )

    fig.update_layout(
        height=600,
        showlegend=False,
        yaxis_title="",
        xaxis_title="Importance Score"
    )

    show_chart(fig, use_container_width=True)

    st.caption(
        "Source: Finalized ExoDetect AI CatBoost model. "
        "Feature importance scores are model-specific."
    )

else:
    st.error("Feature importance file not found.")

st.divider()
# --------------------------------------------------
# 2. GLOBAL SHAP ANALYSIS
# --------------------------------------------------

st.header("2. Global SHAP Analysis")

st.markdown(
    """
    SHAP (SHapley Additive exPlanations) helps us understand
    how individual features influence the model's predictions.

    Mean absolute SHAP values measure the average magnitude
    of a feature's contribution across the analyzed observations.
    """
)

SHAP_PATH = DATA_PATH / "shap_global_importance.csv"


@st.cache_data
def load_global_shap():
    return pd.read_csv(SHAP_PATH)


if SHAP_PATH.exists():

    shap_df = load_global_shap()

    top_shap = st.slider(
        "Number of SHAP features to display",
        min_value=5,
        max_value=31,
        value=15,
        key="shap_slider"
    )

    shap_chart_df = shap_df.head(top_shap).sort_values(
        "mean_abs_shap",
        ascending=True
    )

    fig_shap = px.bar(
        shap_chart_df,
        x="mean_abs_shap",
        y="feature",
        orientation="h",
        title=f"Top {top_shap} Features — Global SHAP Importance",
        labels={
            "mean_abs_shap": "Mean Absolute SHAP Value",
            "feature": "Astronomical Feature"
        },
        template="plotly_dark"
    )

    fig_shap.update_layout(
        height=600,
        showlegend=False,
        yaxis_title="",
        xaxis_title="Mean Absolute SHAP Value"
    )

    show_chart(fig_shap, use_container_width=True)

    st.caption(
        "SHAP analysis was calculated using 100 randomly selected "
        "Kepler test observations. Values explain raw model outputs, "
        "not calibrated probabilities."
    )

    st.info(
        """
        **Why are SHAP and CatBoost rankings different?**

        CatBoost measures feature importance using its internal
        prediction-based importance calculation.

        SHAP measures how much each feature contributes to changing
        the model output across individual observations.

        Therefore, their rankings do not have to be identical.
        """
    )

else:
    st.error("Global SHAP importance file not found.")

st.divider()
# --------------------------------------------------
# 3. CLASS-WISE SHAP ANALYSIS
# --------------------------------------------------

st.header("3. Class-wise SHAP Analysis")

st.markdown(
    """
    Different astronomical features may influence each prediction class
    differently.

    Explore the SHAP importance rankings for each class separately.
    """
)

class_shap_files = {
    "Candidate": DATA_PATH / "shap_candidate_importance.csv",
    "Confirmed": DATA_PATH / "shap_confirmed_importance.csv",
    "False Positive": DATA_PATH / "shap_false_positive_importance.csv"
}

selected_class = st.selectbox(
    "Select a prediction class",
    list(class_shap_files.keys())
)

selected_file = class_shap_files[selected_class]


@st.cache_data
def load_class_shap(file_path):
    return pd.read_csv(file_path)


if selected_file.exists():

    class_shap_df = load_class_shap(str(selected_file))

    class_top_n = st.slider(
        "Number of features to display",
        min_value=5,
        max_value=31,
        value=15,
        key="class_shap_slider"
    )

    class_chart_df = class_shap_df.head(class_top_n).sort_values(
        "mean_abs_shap",
        ascending=True
    )

    fig_class = px.bar(
        class_chart_df,
        x="mean_abs_shap",
        y="feature",
        orientation="h",
        title=f"SHAP Importance — {selected_class}",
        labels={
            "mean_abs_shap": "Mean Absolute SHAP Value",
            "feature": "Astronomical Feature"
        },
        template="plotly_dark"
    )

    fig_class.update_layout(
        height=600,
        showlegend=False,
        yaxis_title="",
        xaxis_title="Mean Absolute SHAP Value"
    )

    show_chart(fig_class, use_container_width=True)

    st.caption(
        f"Class-specific SHAP importance calculated from "
        f"100 Kepler test observations for {selected_class}."
    )

else:
    st.error(f"SHAP file not found for {selected_class}.")

st.divider()
# --------------------------------------------------
# 4. FEATURE ABLATION ANALYSIS
# --------------------------------------------------

st.header("4. Feature Ablation Analysis")

st.markdown(
    """
    Feature ablation is an experiment where we remove a feature
    and measure how the model's performance changes.

    In this experiment, we removed `koi_model_snr` and retrained
    CatBoost using the same training configuration.
    """
)

ABLATION_PATH = DATA_PATH / "feature_ablation_results.json"

if ABLATION_PATH.exists():

    with open(ABLATION_PATH, "r") as file:
        ablation_data = json.load(file)

    baseline_f1 = ablation_data["baseline_macro_f1"]
    ablated_f1 = ablation_data["metrics"]["macro_f1"]

    baseline_accuracy = 0.79467
    ablated_accuracy = ablation_data["metrics"]["accuracy"]

    baseline_features = ablation_data["baseline_features"]
    ablated_features = ablation_data["ablated_features"]

    st.subheader("Model Comparison")

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Original Model Macro F1",
            f"{baseline_f1 * 100:.2f}%",
            help="CatBoost trained using all 31 features."
        )

    with col2:
        st.metric(
            "Without SNR Macro F1",
            f"{ablated_f1 * 100:.2f}%",
            delta=f"{(ablated_f1 - baseline_f1) * 100:.2f} percentage points",
            delta_color="inverse",
            help="CatBoost retrained after removing koi_model_snr."
        )

    comparison_df = pd.DataFrame({
        "Model": [
            "Original CatBoost",
            "Without koi_model_snr"
        ],
        "Macro F1": [
            baseline_f1,
            ablated_f1
        ],
        "Accuracy": [
            baseline_accuracy,
            ablated_accuracy
        ]
    })

    fig_ablation = px.bar(
        comparison_df,
        x="Model",
        y=["Macro F1", "Accuracy"],
        barmode="group",
        title="Performance Before and After Feature Removal",
        template="plotly_dark",
        labels={
            "value": "Score",
            "variable": "Metric"
        },
        text_auto=".3f"
    )

    fig_ablation.update_layout(
        height=450,
        yaxis_range=[0, 1]
    )

    show_chart(fig_ablation, use_container_width=True)

    st.subheader("Feature Count Comparison")

    feature_col1, feature_col2 = st.columns(2)

    with feature_col1:
        st.metric("Original Features", baseline_features)

    with feature_col2:
        st.metric("Features After Removal", ablated_features)

    performance_drop = (baseline_f1 - ablated_f1) * 100

    st.warning(
        f"""
        **Key Finding**

        Removing `koi_model_snr` reduced Macro F1 by
        {performance_drop:.2f} percentage points.

        This demonstrates that the feature contributes
        meaningfully to the predictive performance of ExoDetect AI.
        """
    )

    st.caption(
        "Both models were trained using the same CatBoost "
        "hyperparameters and group-aware data split."
    )

else:
    st.error("Feature ablation results file not found.")

st.divider()

st.success(
    "ExoDetect AI model explainability analysis completed."
)

st.info(
    "This page explains the finalized CatBoost model using "
    "built-in feature importance, SHAP analysis, and feature ablation."
)