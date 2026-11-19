# 🪐 ExoDetect AI
### An Explainable Machine Learning System for Exoplanet Classification

ExoDetect AI is an end-to-end machine learning project that uses astronomical catalogue data from NASA's Kepler mission to classify potential exoplanet observations into three categories:

- **CONFIRMED** — Observations classified as confirmed exoplanets.
- **CANDIDATE** — Observations classified as potential exoplanet candidates.
- **FALSE POSITIVE** — Observations classified as false positive detections.

The project combines machine learning, deep learning, explainable AI, cross-mission validation and an interactive Streamlit application.

---

## 🌌 Project Highlights

- NASA Kepler and TESS catalogue datasets.
- Exploratory Data Analysis and feature engineering.
- Leakage-aware preprocessing and group-aware validation.
- CatBoost and Deep Learning model development.
- SHAP-based model explainability.
- Feature ablation experiments.
- Cross-mission validation using TESS observations.
- Domain shift analysis.
- Interactive Streamlit prediction dashboard.

---

## 🧠 Machine Learning Models

Two primary approaches were investigated:

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| CatBoost | 79.47% | 75.27% |
| Weighted Deep Learning MLP | 69.49% | 66.41% |

### Selected Model: CatBoost

CatBoost was selected as the primary prediction model because it achieved better overall classification performance.

**Final Kepler test performance:**

- Accuracy: 79.47%
- Balanced Accuracy: 74.97%
- Macro Precision: 76.16%
- Macro Recall: 74.97%
- Macro F1: 75.27%

The model uses 31 astronomical input features.

---

## 🔬 Explainable AI

ExoDetect AI incorporates model explainability to investigate which astronomical parameters influence classification.

Implemented techniques:

1. CatBoost Feature Importance
2. SHAP Global Feature Importance
3. Class-wise SHAP Analysis
4. Feature Ablation Experiment

The feature ablation experiment evaluated the effect of removing `koi_model_snr`.

Results:

| Metric | Original Model | Without SNR |
|---|---:|---:|
| Accuracy | 79.47% | 77.38% |
| Balanced Accuracy | 74.97% | 71.85% |
| Macro F1 | 75.27% | 71.98% |

Removing the signal-to-noise feature reduced Macro F1 by approximately 3.29 percentage points.

---

## 🛰️ Cross-Mission Validation

An important experiment investigated whether a model trained using Kepler observations could generalize to TESS observations.

The experiment used nine shared astronomical features and a reduced-feature CatBoost model.

### Kepler vs TESS Results

| Metric | Kepler | TESS |
|---|---:|---:|
| Accuracy | 74.92% | 28.28% |
| Balanced Accuracy | 69.23% | 51.87% |
| Macro F1 | 69.01% | 29.31% |

The substantial performance degradation demonstrates the difficulty of transferring a machine learning model between different astronomical missions.

### Domain Shift Analysis

A Random Forest domain classifier was trained to distinguish Kepler and TESS observations.

Results:

- Domain Classification Accuracy: 90.43%
- Domain Classification ROC-AUC: 96.47%

All nine shared features showed statistically significant distribution differences according to the Kolmogorov-Smirnov tests.

### Important Experimental Limitations

- TESS dispositions were approximately mapped to Kepler classes.
- 1,203 TESS observations were excluded because their dispositions could not be mapped confidently.
- Cross-mission validation used nine shared catalogue features rather than the original 31 features.
- The experiment uses catalogue parameters, not raw photometric light curves.
- Domain shift is a potential contributor to performance degradation, but it does not establish the only cause.

---

## 🖥️ Interactive Application

The project includes a Streamlit application with four main pages.

### 1. Dashboard
Overview of the project, model status and performance metrics.

### 2. Exoplanet Prediction
Enter astronomical parameters manually or load an actual Kepler observation to generate predictions.

### 3. Model Explainability
Explore feature importance, SHAP analysis and feature ablation results.

### 4. Mission Validation
Explore Kepler vs TESS performance, confusion matrices and domain shift analysis.

---

## 🗂️ Project Structure

```text
NASAexoplanet/
│
├── app/
│   ├── app.py
│   ├── components/
│   ├── pages/
│   │   ├── 2_Prediction.py
│   │   ├── 3_Explainability.py
│   │   └── 4_Mission_Validation.py
│   └── utils/
│       ├── model_loader.py
│       └── theme.py
│
├── data/
│   ├── raw/
│   │   ├── kepler/
│   │   └── tess/
│   └── processed/
│
├── models/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 02_eda.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_machine_learning.ipynb
│   ├── 05_deep_learning.ipynb
│   ├── 06_tess_validation.ipynb
│   └── 07_model_finalization_explainability.ipynb
│
├── src/
│
├── requirements.txt
└── README.md
```

---

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.10 or later
- pip
- Git

### Step 1: Clone the Repository

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd NASAexoplanet
```

### Step 2: Create a Virtual Environment

```bash
python -m venv venv
```

Activate it on Windows:

```bash
venv\Scripts\activate
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 4: Prepare the Data and Model Files

Place the required NASA catalogue datasets inside their respective directories:

```text
data/raw/kepler/
data/raw/tess/
```

The trained model and supporting artifacts must also be available in the `models/` directory.

### Step 5: Run the Application

```bash
streamlit run app/app.py
```

The application will open in your browser.

---

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming Language | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, CatBoost |
| Deep Learning | PyTorch |
| Explainable AI | SHAP, CatBoost SHAP Values |
| Visualization | Plotly, Matplotlib |
| Application | Streamlit |
| Development | Jupyter Notebook |

---

## 🔭 Future Improvements

- Incorporate raw astronomical photometric light curves.
- Experiment with CNN and Transformer-based architectures.
- Investigate domain adaptation techniques.
- Improve cross-mission generalization.
- Evaluate probability calibration.
- Explore additional NASA mission datasets.
- Develop a more robust deployment pipeline.

---

## ⚠️ Scientific Disclaimer

ExoDetect AI is an experimental machine learning system for astronomical catalogue classification.

Its predictions are not independent astronomical confirmations or discoveries. Model outputs should be interpreted alongside scientific validation and the limitations of the underlying datasets.

---

## 👨‍💻 Project

**ExoDetect AI — NASA Exoplanet Classification Using Machine Learning**

An end-to-end exploration of machine learning, explainable AI and cross-mission generalization in exoplanet research.