# 🪐 ExoDetect AI
### Explainable Machine Learning for NASA Exoplanet Classification

[**Live Demo**](https://exoplanetdetect-ai.streamlit.app/) · [**GitHub Repository**](https://github.com/subash-29/ExoDetect-AI)

ExoDetect AI is an end-to-end machine learning project that investigates the classification of astronomical observations using NASA's Kepler and TESS mission catalogue data.

The system classifies Kepler observations into three categories:

- **CONFIRMED** — Observations labelled as confirmed exoplanets.
- **CANDIDATE** — Potential exoplanet candidates.
- **FALSE POSITIVE** — Observations classified as false positive detections.

The project combines classical machine learning, deep learning, explainable AI, cross-mission validation and an interactive Streamlit application.

---

## 🌌 Key Features

- NASA Kepler and TESS catalogue data analysis.
- Exploratory Data Analysis and feature engineering.
- Leakage-aware preprocessing and group-aware validation.
- CatBoost and weighted Deep Learning MLP experiments.
- SHAP-based model explainability.
- Feature ablation experiments.
- Cross-mission validation using TESS observations.
- Domain shift analysis.
- Interactive prediction dashboard.
- Cloud deployment using Streamlit Community Cloud.

## 🧠 Model Performance

Two primary modelling approaches were evaluated.

| Model | Accuracy | Macro F1 |
|---|---:|---:|
| CatBoost | 79.47% | 75.27% |
| Weighted Deep Learning MLP | 69.49% | 66.41% |

### Selected Model: CatBoost

CatBoost was selected as the primary prediction model because it achieved stronger classification performance.

**Final Kepler test results:**

| Metric | Score |
|---|---:|
| Accuracy | 79.47% |
| Balanced Accuracy | 74.97% |
| Macro Precision | 76.16% |
| Macro Recall | 74.97% |
| Macro F1 | 75.27% |

The model uses 31 astronomical input features.

## 🔬 Explainable AI

ExoDetect AI uses explainability techniques to investigate which astronomical parameters influence model predictions.

Implemented techniques:

1. CatBoost feature importance.
2. SHAP global feature importance.
3. Class-wise SHAP analysis.
4. Feature ablation experiments.

### Feature Ablation: Signal-to-Noise Ratio

The experiment evaluated the impact of removing `koi_model_snr`.

| Metric | Original Model | Without SNR |
|---|---:|---:|
| Accuracy | 79.47% | 77.38% |
| Balanced Accuracy | 74.97% | 71.85% |
| Macro F1 | 75.27% | 71.98% |

Removing this feature reduced Macro F1 by approximately 3.29 percentage points.

## 🛰️ Cross-Mission Validation: Kepler vs TESS

An important experiment investigated whether a model trained using Kepler observations could generalize to TESS observations.

The experiment used nine shared astronomical features and a reduced-feature CatBoost model.

| Metric | Kepler | TESS |
|---|---:|---:|
| Accuracy | 74.92% | 28.28% |
| Balanced Accuracy | 69.23% | 51.87% |
| Macro F1 | 69.01% | 29.31% |

The performance degradation highlights the difficulty of transferring a machine learning model between different astronomical missions.

### Domain Shift Analysis

A Random Forest domain classifier was trained to distinguish Kepler and TESS observations.

- Domain classification accuracy: **90.43%**
- Domain classification ROC-AUC: **96.47%**

All nine shared features showed statistically significant distribution differences according to Kolmogorov–Smirnov tests.

### Experimental Limitations

- TESS dispositions were approximately mapped to Kepler classes.
- 1,203 TESS observations were excluded because their dispositions could not be mapped confidently.
- Cross-mission validation used nine shared catalogue features instead of the original 31 features.
- The experiment used catalogue parameters, not raw photometric light curves.
- Domain shift may contribute to performance degradation, but it does not establish the only cause.

## 🖥️ Interactive Application

**Live application:** https://exoplanetdetect-ai.streamlit.app/

The application contains four pages:

| Page | Functionality |
|---|---|
| Dashboard | Project overview and model performance |
| Prediction | Manual feature input and actual Kepler observation loading |
| Explainability | SHAP analysis and feature importance |
| Mission Validation | Kepler–TESS comparison and domain shift analysis |

## 🏗️ Project Workflow

1. Collect and understand NASA catalogue datasets.
2. Perform exploratory data analysis.
3. Preprocess features and prepare group-aware train/test splits.
4. Train and evaluate machine learning models.
5. Experiment with deep learning.
6. Validate using TESS observations.
7. Perform SHAP analysis and feature ablation.
8. Finalize the prediction pipeline.
9. Build and deploy the Streamlit application.

## 🗂️ Repository Structure

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
│   ├── processed/
│   └── lightcurves/
│
├── models/
│
├── notebooks/
│   ├── 01_data_collection.ipynb
│   ├── 01_dataset_understanding.ipynb
│   ├── 03_preprocessing.ipynb
│   ├── 04_machine_learning.ipynb
│   ├── 05_deep_learning.ipynb
│   ├── 06_tess_validation.ipynb
│   └── 07_model_finalization_explainability.ipynb
│
├── src/
├── requirements.txt
└── README.md
```

## ⚙️ Installation and Setup

### Prerequisites

- Python 3.12
- Git
- pip

### 1. Clone the repository

```bash
git clone https://github.com/subash-29/ExoDetect-AI.git
cd ExoDetect-AI
```

### 2. Create a virtual environment

```bash
python -m venv venv
```

Activate on Windows:

```bash
venv\Scripts\activate
```

Activate on Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Verify project data and model artifacts

Ensure the required model artifacts are available in `models/` and the Kepler catalogue is available in:

```text
data/raw/kepler/
```

The TESS validation outputs and other processed artifacts are maintained under `data/processed/` and `models/`.

### 5. Run the application

```bash
streamlit run app/app.py
```

## 🛠️ Technology Stack

| Category | Technologies |
|---|---|
| Programming | Python |
| Data Processing | Pandas, NumPy |
| Machine Learning | Scikit-learn, CatBoost |
| Deep Learning | PyTorch |
| Explainable AI | SHAP |
| Visualization | Plotly, Matplotlib |
| Application | Streamlit |
| Development | Jupyter Notebook |

## 🔭 Future Improvements

- Incorporate raw astronomical photometric light curves.
- Experiment with CNN and Transformer architectures.
- Investigate domain adaptation techniques.
- Improve cross-mission generalization.
- Evaluate probability calibration.
- Explore additional NASA mission datasets.

## ⚠️ Scientific Disclaimer

ExoDetect AI is an experimental machine learning system for astronomical catalogue classification.

Its predictions are not independent astronomical confirmations or discoveries. Model outputs should be interpreted alongside scientific validation and the limitations of the underlying datasets.

## 👨‍💻 Project

**ExoDetect AI — NASA Exoplanet Classification Using Machine Learning**

An end-to-end exploration of machine learning, deep learning, explainable AI and cross-mission generalization in exoplanet research.