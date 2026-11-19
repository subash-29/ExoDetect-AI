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
import plotly.graph_objects as go
from pathlib import Path

# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Mission Validation | ExoDetect AI",
    page_icon="🌌",
    layout="wide"
)

apply_theme()

sidebar_brand()


# --------------------------------------------------
# PROJECT PATHS
# --------------------------------------------------

PROJECT_ROOT = Path(__file__).resolve().parents[2]

DATA_PATH = PROJECT_ROOT / "data" / "processed"
MODEL_PATH = PROJECT_ROOT / "models"

VALIDATION_PATH = MODEL_PATH / "tess_validation_results.json"

# --------------------------------------------------
# LOAD VALIDATION RESULTS
# --------------------------------------------------

@st.cache_data
def load_validation_results():

    with open(VALIDATION_PATH, "r") as file:
        return json.load(file)


results = load_validation_results()

# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

page_hero(
    "🌌",
    "Cross-Mission Validation",
    "Investigating whether a machine learning model trained "
    "on NASA Kepler observations can generalize to NASA TESS observations.",
    "Kepler → TESS"
)

st.divider()

# --------------------------------------------------
# 1. MISSION OVERVIEW
# --------------------------------------------------

st.header("1. Mission Overview")

st.markdown(
    """
    ExoDetect AI uses Kepler observations for model training
    and evaluates cross-mission generalization using TESS data.

    This experiment uses nine shared astronomical features
    mapped between the two mission catalogues.
    """
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Kepler Training Samples",
        f"{results['training_samples']:,}"
    )

with col2:
    st.metric(
        "Kepler Test Samples",
        f"{results['kepler_test_samples']:,}"
    )

with col3:
    st.metric(
        "TESS Validation Samples",
        f"{results['tess_validation_samples']:,}"
    )

col4, col5 = st.columns(2)

with col4:
    st.metric(
        "TESS Excluded Samples",
        f"{results['excluded_tess_samples']:,}"
    )

with col5:
    st.metric(
        "Shared Features",
        len(results["features_used"])
    )

st.divider()

# --------------------------------------------------
# 2. TESS VALIDATION METRICS
# --------------------------------------------------

st.header("2. TESS External Validation Performance")

st.markdown(
    """
    The reduced-feature CatBoost model was trained using Kepler
    data and evaluated on TESS observations without training
    or tuning on the TESS validation dataset.
    """
)

metrics = results["metrics"]

metric1, metric2, metric3 = st.columns(3)

with metric1:
    st.metric(
        "Accuracy",
        f"{metrics['accuracy'] * 100:.2f}%"
    )

with metric2:
    st.metric(
        "Balanced Accuracy",
        f"{metrics['balanced_accuracy'] * 100:.2f}%"
    )

with metric3:
    st.metric(
        "Macro F1",
        f"{metrics['macro_f1'] * 100:.2f}%"
    )

st.divider()
# --------------------------------------------------
# 3. KEPLER VS TESS PERFORMANCE COMPARISON
# --------------------------------------------------

st.header("3. Kepler vs TESS Performance Comparison")

st.markdown(
    """
    We compare the performance of the same reduced-feature
    CatBoost model on the Kepler test dataset and the external
    TESS validation dataset.

    This helps us understand how well the model generalizes
    across different NASA missions.
    """
)

comparison_df = pd.DataFrame({
    "Metric": [
        "Accuracy",
        "Balanced Accuracy",
        "Macro F1"
    ],
    "Kepler": [
        0.749216,
        0.692253,
        0.690093
    ],
    "TESS": [
        results["metrics"]["accuracy"],
        results["metrics"]["balanced_accuracy"],
        results["metrics"]["macro_f1"]
    ]
})

comparison_long = comparison_df.melt(
    id_vars="Metric",
    var_name="Mission",
    value_name="Score"
)

fig_comparison = px.bar(
    comparison_long,
    x="Metric",
    y="Score",
    color="Mission",
    barmode="group",
    text_auto=".3f",
    title="Reduced-Feature CatBoost: Kepler vs TESS",
    template="plotly_dark"
)

fig_comparison.update_layout(
    height=500,
    yaxis_title="Performance Score",
    yaxis_range=[0, 1]
)

show_chart(
    fig_comparison,
    use_container_width=True
)

st.info(
    """
    **Key Observation**

    The model performs substantially better on Kepler than TESS.
    This indicates a significant cross-mission generalization
    challenge.
    """
)

st.caption(
    "Both evaluations use the same nine mapped features. "
    "Kepler metrics are from the reduced-feature model, not "
    "the original 31-feature model."
)

st.divider()
# --------------------------------------------------
# 4. TESS CONFUSION MATRIX
# --------------------------------------------------

st.header("4. TESS Confusion Matrix")

st.markdown(
    """
    A confusion matrix helps us understand how the model's
    predictions compare with the actual TESS classifications.
    """
)

confusion_matrix = np.array(results["confusion_matrix"])

class_names = [
    "CANDIDATE",
    "CONFIRMED",
    "FALSE POSITIVE"
]

fig_cm = px.imshow(
    confusion_matrix,
    x=class_names,
    y=class_names,
    text_auto=True,
    color_continuous_scale=["#0B1426", "#1D4ED8", "#56CFE1"],
    aspect="auto",
    title="TESS External Validation Confusion Matrix"
)

fig_cm.update_layout(
    height=500,
    xaxis_title="Predicted Class",
    yaxis_title="Actual Class",
    template="plotly_dark"
)

show_chart(
    fig_cm,
    use_container_width=True
)

st.caption(
    "Rows represent actual classes; columns represent predicted classes."
)

# --------------------------------------------------
# CLASS-WISE PERFORMANCE
# --------------------------------------------------

st.subheader("Class-wise Performance")

report = results["classification_report"]

class_performance = pd.DataFrame([
    {
        "Class": class_name,
        "Precision": report[class_name]["precision"],
        "Recall": report[class_name]["recall"],
        "F1 Score": report[class_name]["f1-score"],
        "Support": int(report[class_name]["support"])
    }
    for class_name in class_names
])

st.dataframe(
    class_performance.style.format({
        "Precision": "{:.3f}",
        "Recall": "{:.3f}",
        "F1 Score": "{:.3f}"
    }),
    use_container_width=True,
    hide_index=True
)

st.warning(
    """
    **Important Finding**

    Candidate recall is only 8.44%.

    The model identifies very few actual TESS Candidates correctly,
    highlighting the difficulty of transferring Kepler-trained
    decision patterns to TESS observations.
    """
)

st.divider()
# --------------------------------------------------
# 5. DOMAIN SHIFT ANALYSIS
# --------------------------------------------------

st.header("5. Domain Shift Analysis")

st.markdown(
    """
    Domain shift occurs when the statistical distribution of
    input features changes between the training and deployment
    datasets.

    Here, we investigate differences between Kepler and TESS
    using the Kolmogorov-Smirnov (KS) statistical test.
    """
)

DOMAIN_SHIFT_PATH = DATA_PATH / "domain_shift_summary.csv"

@st.cache_data
def load_domain_shift():
    return pd.read_csv(DOMAIN_SHIFT_PATH)

domain_df = load_domain_shift()

# --------------------------------------------------
# 5.1 KS STATISTIC
# --------------------------------------------------

st.subheader("5.1 Feature Distribution Differences")

st.markdown(
    """
    The KS statistic measures the maximum difference between
    the cumulative distributions of two datasets.

    Higher values indicate greater distribution differences.
    """
)

ks_plot_df = domain_df.sort_values(
    "KS Statistic",
    ascending=True
)

fig_ks = px.bar(
    ks_plot_df,
    x="KS Statistic",
    y="Feature",
    orientation="h",
    text_auto=".3f",
    color="KS Statistic",
    color_continuous_scale=["#2A3F66", "#8B7CF6", "#56CFE1"],
    title="Kepler vs TESS: KS Statistics",
    template="plotly_dark"
)

fig_ks.update_layout(height=500, coloraxis_showscale=False)

show_chart(
    fig_ks,
    use_container_width=True
)

# --------------------------------------------------
# 5.2 MEDIAN COMPARISON
# --------------------------------------------------

st.subheader("5.2 Feature Median Comparison")

selected_feature = st.selectbox(
    "Select a feature",
    domain_df["Feature"].tolist()
)

selected_row = domain_df[
    domain_df["Feature"] == selected_feature
].iloc[0]

median_comparison = pd.DataFrame({
    "Mission": ["Kepler", "TESS"],
    "Median": [
        selected_row["Kepler Median"],
        selected_row["TESS Median"]
    ]
})

fig_median = px.bar(
    median_comparison,
    x="Mission",
    y="Median",
    text_auto=".3f",
    title=f"Median Comparison: {selected_feature}",
    template="plotly_dark"
)

show_chart(
    fig_median,
    use_container_width=True
)

# --------------------------------------------------
# 5.3 DOMAIN CLASSIFIER
# --------------------------------------------------

st.subheader("5.3 Domain Classifier Performance")

domain_results = results["domain_classifier"]

col1, col2 = st.columns(2)

col1.metric(
    "Domain Classifier Accuracy",
    f"{domain_results['accuracy']:.2%}"
)

col2.metric(
    "Domain Classifier ROC-AUC",
    f"{domain_results['roc_auc']:.2%}"
)

st.info(
    """
    **Interpretation**

    The domain classifier can distinguish Kepler and TESS
    observations with high accuracy.

    This indicates that the two missions have substantially
    different feature distributions, which may contribute
    to the model's cross-mission generalization difficulty.

    However, domain shift alone does not prove the cause
    of the performance decline.
    """
)

st.divider()
# --------------------------------------------------
# 6. SCIENTIFIC FINDINGS AND LIMITATIONS
# --------------------------------------------------

st.header("6. Scientific Findings and Limitations")

st.markdown(
    """
    This section summarizes the major findings from the
    cross-mission validation experiment.
    """
)

# --------------------------------------------------
# 6.1 KEY FINDINGS
# --------------------------------------------------

st.subheader("6.1 Key Findings")

findings = [
    {
        "title": "Significant Performance Degradation",
        "description": (
            "The reduced-feature model achieved a Macro F1 score "
            "of 69.01% on Kepler but only 29.31% on TESS. "
            "This demonstrates poor cross-mission generalization."
        )
    },
    {
        "title": "Candidate Detection Challenge",
        "description": (
            "Candidate recall on TESS was only 8.44%. "
            "The model failed to correctly identify most "
            "observations belonging to this class."
        )
    },
    {
        "title": "Substantial Feature Distribution Differences",
        "description": (
            "All nine shared features showed statistically "
            "significant distribution differences according "
            "to the KS tests."
        )
    },
    {
        "title": "Mission Identification Is Possible",
        "description": (
            "The domain classifier achieved 90.43% accuracy "
            "and 96.47% ROC-AUC, showing that Kepler and TESS "
            "observations are distinguishable using their "
            "catalogue features."
        )
    }
]

for finding in findings:
    with st.expander(finding["title"]):
        st.write(finding["description"])

# --------------------------------------------------
# 6.2 EXPERIMENTAL LIMITATIONS
# --------------------------------------------------

st.subheader("6.2 Experimental Limitations")

limitations = [
    (
        "Different Mission Characteristics",
        "Kepler and TESS have different observational characteristics "
        "and catalogue distributions."
    ),
    (
        "Approximate Label Mapping",
        "TESS PC, CP and FP were mapped to Kepler CANDIDATE, "
        "CONFIRMED and FALSE POSITIVE respectively. These labels "
        "are not guaranteed to have identical scientific meanings."
    ),
    (
        "Excluded TESS Observations",
        "A total of 1,203 TESS observations were excluded because "
        "their dispositions could not be mapped confidently."
    ),
    (
        "Reduced Feature Set",
        "Cross-mission validation used nine shared catalogue features "
        "instead of the original 31 Kepler features."
    ),
    (
        "Catalogue-Level Analysis",
        "This experiment uses catalogue parameters rather than "
        "raw photometric light curves."
    ),
    (
        "Distribution Shift Is Not the Only Possible Cause",
        "Differences in label definitions, measurement procedures, "
        "selection effects and class distributions may also "
        "contribute to performance degradation."
    )
]

for title, description in limitations:
    with st.expander(title):
        st.write(description)

# --------------------------------------------------
# 6.3 FINAL CONCLUSION
# --------------------------------------------------

st.subheader("6.3 Conclusion")

st.success(
    """
    ExoDetect AI demonstrates promising exoplanet disposition
    classification performance on Kepler observations.

    However, external validation on TESS reveals substantial
    performance degradation, highlighting the challenges of
    transferring machine learning models across astronomical
    missions.

    The experiment demonstrates the importance of cross-mission
    validation, domain shift analysis and careful interpretation
    of astronomical classification labels.
    """
)

st.caption(
    "Research note: These results evaluate catalogue-level "
    "classification and should not be interpreted as independent "
    "confirmation of newly discovered exoplanets."
)

st.divider()