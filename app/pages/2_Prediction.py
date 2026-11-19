import sys
from pathlib import Path

import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np

PROJECT_ROOT = Path(__file__).resolve().parents[2]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.utils.model_loader import load_prediction_model
from app.utils.theme import apply_theme, page_hero


# --------------------------------------------------
# PAGE CONFIGURATION
# --------------------------------------------------

st.set_page_config(
    page_title="Exoplanet Prediction | ExoDetect AI",
    page_icon="🔭",
    layout="wide"
)


# --------------------------------------------------
# CUSTOM CSS
# --------------------------------------------------

apply_theme()


# --------------------------------------------------
# MODEL LOADING
# --------------------------------------------------

@st.cache_resource
def get_artifact():
    return load_prediction_model()


try:
    artifact = get_artifact()

    pipeline = artifact["pipeline"]
    feature_names = artifact["feature_names"]
    target_classes = artifact["target_classes"]

    imputer = pipeline.named_steps["imputer"]

    median_values = dict(
        zip(feature_names, imputer.statistics_)
    )

except Exception as error:
    st.error(f"Unable to load prediction model: {error}")
    st.stop()


# --------------------------------------------------
# FEATURE INFORMATION
# --------------------------------------------------

feature_information = {

    "koi_period": (
        "Orbital Period",
        "Days",
        "Time taken by a planet to complete one orbit around its host star."
    ),

    "koi_time0bk": (
        "Transit Epoch (BKJD)",
        "Days",
        "Reference time of the transit in the BKJD time system."
    ),

    "koi_time0": (
        "Transit Epoch (BJD)",
        "Days",
        "Reference time of the transit in Barycentric Julian Date."
    ),

    "koi_impact": (
        "Impact Parameter",
        "Dimensionless",
        "Describes how centrally the planet crosses the stellar disc."
    ),

    "koi_duration": (
        "Transit Duration",
        "Hours",
        "Time taken by the planet to pass across its host star."
    ),

    "koi_depth": (
        "Transit Depth",
        "ppm",
        "Reduction in observed stellar brightness during a planetary transit."
    ),

    "koi_ror": (
        "Planet-to-Star Radius Ratio",
        "Dimensionless",
        "Ratio between the planet's radius and the host star's radius."
    ),

    "koi_srho": (
        "Stellar Density",
        "g/cm³",
        "Estimated density of the host star."
    ),

    "koi_prad": (
        "Planetary Radius",
        "Earth radii",
        "Estimated radius of the planet relative to Earth's radius."
    ),

    "koi_sma": (
        "Semi-Major Axis",
        "AU",
        "Average orbital distance between the planet and its host star."
    ),

    "koi_incl": (
        "Orbital Inclination",
        "Degrees",
        "Angle of the planetary orbital plane relative to our line of sight."
    ),

    "koi_teq": (
        "Equilibrium Temperature",
        "Kelvin",
        "Estimated planetary temperature assuming radiative equilibrium."
    ),

    "koi_insol": (
        "Insolation Flux",
        "Earth flux",
        "Stellar energy received by the planet relative to Earth."
    ),

    "koi_dor": (
        "Scaled Orbital Distance",
        "Dimensionless",
        "Ratio of orbital distance to stellar radius."
    ),

    "koi_ldm_coeff2": (
        "Limb Darkening Coefficient 2",
        "Dimensionless",
        "Second coefficient describing the variation in brightness across the stellar disc."
    ),

    "koi_ldm_coeff1": (
        "Limb Darkening Coefficient 1",
        "Dimensionless",
        "First coefficient describing the variation in brightness across the stellar disc."
    ),

    "koi_model_snr": (
        "Transit Model Signal-to-Noise Ratio",
        "Dimensionless",
        "Measures how clearly the transit signal can be distinguished from noise."
    ),

    "koi_count": (
        "Number of Planet Candidates",
        "Count",
        "Number of planet candidates associated with the same host star."
    ),

    "koi_steff": (
        "Stellar Effective Temperature",
        "Kelvin",
        "Effective surface temperature of the host star."
    ),

    "koi_slogg": (
        "Stellar Surface Gravity",
        "log10(cm/s²)",
        "Logarithmic measurement of the host star's surface gravity."
    ),

    "koi_smet": (
        "Stellar Metallicity",
        "dex",
        "Metal abundance of the host star relative to the Sun."
    ),

    "koi_srad": (
        "Stellar Radius",
        "Solar radii",
        "Radius of the host star relative to the Sun."
    ),

    "koi_smass": (
        "Stellar Mass",
        "Solar masses",
        "Mass of the host star relative to the Sun."
    ),

    "koi_kepmag": (
        "Kepler Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the Kepler photometric band."
    ),

    "koi_gmag": (
        "Gaia G Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the Gaia G-band."
    ),

    "koi_rmag": (
        "Sloan r Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the Sloan r-band."
    ),

    "koi_imag": (
        "Sloan i Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the Sloan i-band."
    ),

    "koi_zmag": (
        "Sloan z Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the Sloan z-band."
    ),

    "koi_jmag": (
        "2MASS J Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the 2MASS J-band."
    ),

    "koi_hmag": (
        "2MASS H Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the 2MASS H-band."
    ),

    "koi_kmag": (
        "2MASS K Magnitude",
        "Magnitude",
        "Apparent brightness of the star in the 2MASS K-band."
    )
}


# --------------------------------------------------
# FEATURE GROUPS
# --------------------------------------------------

sections = {

    "Orbital Parameters": {
        "description": "Parameters describing the planet's orbital motion.",
        "features": [
            "koi_period",
            "koi_time0bk",
            "koi_time0",
            "koi_impact",
            "koi_duration",
            "koi_sma",
            "koi_incl",
            "koi_dor"
        ]
    },

    "Planetary Parameters": {
        "description": "Measurements describing the potential planet and its transit.",
        "features": [
            "koi_depth",
            "koi_ror",
            "koi_prad",
            "koi_teq",
            "koi_insol"
        ]
    },

    "Stellar Parameters": {
        "description": "Physical properties of the host star.",
        "features": [
            "koi_srho",
            "koi_steff",
            "koi_slogg",
            "koi_smet",
            "koi_srad",
            "koi_smass",
            "koi_count"
        ]
    },

    "Additional Parameters": {
        "description": "Transit model characteristics and stellar brightness measurements.",
        "features": [
            "koi_ldm_coeff2",
            "koi_ldm_coeff1",
            "koi_model_snr",
            "koi_kepmag",
            "koi_gmag",
            "koi_rmag",
            "koi_imag",
            "koi_zmag",
            "koi_jmag",
            "koi_hmag",
            "koi_kmag"
        ]
    }
}


# --------------------------------------------------
# KEPLER EXAMPLE DATA
# --------------------------------------------------


@st.cache_data
def load_kepler_examples():

    data_directory = PROJECT_ROOT / "data" / "raw" / "kepler"
    print("PROJECT ROOT:", PROJECT_ROOT)
    print("DATA DIRECTORY:", data_directory)
    print("DIRECTORY EXISTS:", data_directory.exists())
    print("CSV FILES FOUND:", list(data_directory.glob("*.csv")))

    files = list(data_directory.glob("*.csv"))

    if not files:
        return None

    csv_file = files[0]

    # Automatically locate the actual CSV header
    header_row = None

    with open(csv_file, "r", encoding="utf-8-sig") as file:

        for index, line in enumerate(file):

            if line.strip().startswith("rowid,kepid,"):

                header_row = index
                break

    if header_row is None:
        raise ValueError("Could not locate the Kepler CSV header.")

    # Load only the features required by our model
    required_columns = set(feature_names) | {"kepid"}

    df = pd.read_csv(
        csv_file,
        skiprows=header_row,
        usecols=lambda column: column in required_columns,
        low_memory=False
    )

    if df.empty:
        raise ValueError("The Kepler dataset contains no observations.")

    return df



# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

with st.sidebar:

    st.title("🪐 ExoDetect AI")

    st.caption("NASA Exoplanet Detection System")

    st.divider()

    st.page_link("app.py", label="Dashboard", icon="🏠")

    st.markdown("### Prediction Model")

    st.success("CatBoost Model Online")

    st.caption("31 astronomical input features")


# --------------------------------------------------
# PAGE HEADER
# --------------------------------------------------

page_hero(
    "🔭",
    "Exoplanet Prediction",
    "Explore astronomical parameters and classify potential "
    "exoplanet observations using the trained CatBoost model.",
    "Live CatBoost Inference"
)

st.info(
    "You can enter parameters manually, load a real Kepler "
    "observation, or restore the training-set median values."
)


# --------------------------------------------------
# EXAMPLE OBSERVATION AND RESET
# --------------------------------------------------

st.markdown("## Input Configuration")

example_df = load_kepler_examples()

col1, col2 = st.columns([2, 1])


with col1:

    if example_df is not None:

        sample_index = st.number_input(
            "Kepler observation row index",
            min_value=0,
            max_value=len(example_df) - 1,
            value=0,
            step=1
        )

        if st.button("Load Kepler Observation", use_container_width=True):

            sample = example_df.iloc[int(sample_index)]

            for feature in feature_names:

                value = sample[feature]

                st.session_state[f"input_{feature}"] = (
                    float(value)
                    if pd.notna(value)
                    else float(median_values[feature])
                )

    else:
        st.info(
            "Kepler sample loading is unavailable in the cloud deployment. "
            "You can still enter feature values manually or use the default "
            "median values to make predictions."
        )
with col2:

    if st.button("↩ Reset All Parameters", use_container_width=True):

        for feature in feature_names:

            st.session_state[f"input_{feature}"] = float(
                median_values[feature]
            )

        st.session_state["loaded_sample"] = False

        st.rerun()


# --------------------------------------------------
# INPUT FORM
# --------------------------------------------------

st.markdown("---")

st.markdown("## Astronomical Parameters")

st.caption(
    "Enter all 31 parameters. Hover over the information icons "
    "to understand each feature."
)

input_values = {}

with st.form("prediction_form"):

    for section_name, section_data in sections.items():

        st.markdown(f"### {section_name}")

        st.caption(section_data["description"])

        features = section_data["features"]

        columns = st.columns(2)

        for index, feature in enumerate(features):

            name, unit, description = feature_information[feature]

            with columns[index % 2]:

                key = f"input_{feature}"

                value = st.number_input(
                    label=f"{name} ({unit})",
                    value=float(
                        st.session_state.get(
                            key,
                            median_values[feature]
                        )
                    ),
                    help=description,
                    format="%.6f",
                    key=key
                )

                input_values[feature] = value

        st.markdown("---")

    submitted = st.form_submit_button(
        "🚀 Predict Exoplanet Classification",
        use_container_width=True
    )


# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

# --------------------------------------------------
# PREDICTION
# --------------------------------------------------

if submitted:

    input_df = pd.DataFrame(
        [[input_values[feature] for feature in feature_names]],
        columns=feature_names
    )

    try:

        # Generate prediction
        raw_prediction = pipeline.predict(input_df)

        # Convert NumPy output into a standard Python string
        prediction = str(np.asarray(raw_prediction).reshape(-1)[0])

        # Generate class probabilities
        probabilities = np.asarray(
            pipeline.predict_proba(input_df)
        ).reshape(-1)

        # Convert probabilities into standard Python floats
        probabilities = [float(value) for value in probabilities]

        probability_df = pd.DataFrame({

            "Class": [str(class_name) for class_name in target_classes],

            "Probability (%)": [
                round(value * 100, 2)
                for value in probabilities
            ]

        })

        st.markdown("---")

        st.markdown("## 🪐 Prediction Result")

        class_colors = {
            "CANDIDATE": "#F5B942",
            "CONFIRMED": "#3DDC97",
            "FALSE POSITIVE": "#FF6B81"
        }

        accent = class_colors.get(prediction, "#56CFE1")

        st.markdown(
            f'<div class="result-card" style="--accent:{accent};">'
            '<div class="result-label">CatBoost predicted classification</div>'
            f'<div class="result-title">{prediction}</div>'
            f'<div class="result-conf">Highest class score: '
            f'{max(probabilities) * 100:.2f}%</div>'
            '</div>',
            unsafe_allow_html=True
        )

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Highest Class Probability",
                f"{max(probabilities) * 100:.2f}%"
            )

        with col2:

            st.metric(
                "Predicted Classification",
                prediction
            )

        st.markdown("### Class Probability Distribution")

        fig = px.bar(
            probability_df,
            x="Class",
            y="Probability (%)",
            text="Probability (%)",
            color="Class",
            color_discrete_map=class_colors,
            title="CatBoost Classification Scores"
        )

        fig.update_traces(textposition="outside")

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Inter, sans-serif", color="#E6EDF7"),
            showlegend=False,
            yaxis_range=[0, 110],
            margin=dict(l=20, r=20, t=60, b=20)
        )

        fig.update_yaxes(
            gridcolor="rgba(120,140,180,0.15)",
            zeroline=False
        )

        st.plotly_chart(
            fig,
            use_container_width=True
        )

        st.markdown("### Detailed Prediction Scores")

        st.dataframe(
            probability_df,
            use_container_width=True,
            hide_index=True
        )

        st.markdown("### Interpretation")

        explanations = {

            "CANDIDATE":
                "The model classifies this observation as a planet candidate. "
                "Further astronomical validation is required.",

            "CONFIRMED":
                "The model classifies this observation as confirmed. "
                "This is a model prediction, not independent scientific confirmation.",

            "FALSE POSITIVE":
                "The model classifies this observation as a false positive, "
                "suggesting that the detected transit may not be caused by a planet."
        }

        st.info(explanations[prediction])

        st.warning(
            "Important: Model scores are not independently calibrated "
            "probabilities. Predictions should not be treated as "
            "astronomical discoveries or independent confirmation."
        )

    except Exception as error:

        st.error(f"Prediction failed: {error}")

# --------------------------------------------------
# FOOTER
# --------------------------------------------------

st.markdown("---")

st.caption(
    "ExoDetect AI | NASA Kepler Mission | CatBoost Classification"
)