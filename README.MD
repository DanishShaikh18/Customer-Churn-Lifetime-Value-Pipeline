# H&M Customer Intelligence Pipeline
### Churn Prediction & Lifetime Value Forecasting · SQL → Python → Power BI

---

## Overview

End-to-end customer analytics pipeline built on real H&M commercial transaction data.
Covers behavioral segmentation, survival-based churn prediction, and LTV forecasting —
with a SQL engineering layer, Python ML stack, statistical validation, and a Power BI
executive dashboard quantifying revenue at risk per customer segment.

---

## Dataset

| File | Rows | Note |
|---|---|---|
| transactions_train.csv | 3.17 crore | Raw, gitignored |
| transactions_sample.csv | 51 lakh | 17% customer sample, seed=42 |
| customers_sample.csv | 2.2 lakh | Matched to sampled customers |
| articles.csv | 1.05 lakh | Full file, no sampling needed |

**Source:** [H&M Personalized Fashion Recommendations — Kaggle](https://www.kaggle.com/competitions/h-and-m-personalized-fashion-recommendations/data)  
**Date range:** September 2018 – September 2020  
**Why sampled?** Raw transactions file is 3.5 GB. Sampled by customer ID (not rows)
so every customer's purchase history stays 100% intact.

---

## Project Structure
hm-customer-analytics/
├── data/
│   ├── raw/                    ← original H&M CSVs (gitignored)
│   └── processed/              ← all pipeline outputs
├── sql/                        ← SQL files, numbered in order
├── src/                        ← one Python script per module
├── outputs/
│   ├── plots/                  ← all charts saved as .png
│   └── models/                 ← saved model files
├── tests/                      ← pytest test suite
├── powerbi/                    ← dashboard.pbix
├── docs/                       ← DAX documentation
├── Dockerfile
├── requirements.txt
└── run_pipeline.sh

---

## Tech Stack

| Layer | Tools |
|---|---|
| Data Engineering | DuckDB, SQL |
| Analysis & ML | Python, Pandas, Scikit-learn, Lifelines, LightGBM, Optuna, SHAP |
| Statistics | Scipy, Statsmodels |
| Visualization | Matplotlib, Seaborn, Power BI |
| Testing | Pytest |
| Infra | Docker |

---

## How to Run

**Step 0 — Setup**
```bash
git clone https://github.com/DanishShaikh18/hm-customer-analytics
cd hm-customer-analytics
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

**Step 1 — Add raw data**  
Download the three CSVs from Kaggle and place them in `data/raw/`

**Step 2 — Sample the dataset (run once)**
```bash
python src/00_sample_data.py
```

**Step 3 — Run the full pipeline**
```bash
bash run_pipeline.sh
```

---

## Pipeline Modules

| Module | Script | What it does |
|---|---|---|
| Data Engineering | `01_data_engineering.py` | SQL layer, RFM, cohort table, data quality report |
| EDA | `02_eda.py` | Distribution analysis, statistical tests, Lorenz curve |
| Segmentation | `03_segmentation.py` | K-Means + Gaussian Mixture Models |
| Churn Model | `04_churn_model.py` | Survival analysis, Cox PH, calibration |
| LTV Model | `05_ltv_model.py` | LightGBM, Optuna tuning, SHAP explainability |
| Dashboard Export | `06_export_dashboard.py` | Final CSVs for Power BI |

---

## Model Performance

| Model | Metric | Train | Test |
|---|---|---|---|
| Cox PH Churn | C-Index | — | — |
| LightGBM LTV | RMSE | — | — |
| LightGBM LTV | AWRMSE | — | — |

*To be updated after training*

---

## Key Findings

*To be updated after each module completes*

- Segmentation: X customer segments identified
- Churn: High-risk segment churn probability of X%
- LTV: Top segment predicted 12-month LTV of ₹X
- Revenue at risk: ₹X across high-LTV, high-churn segment

---

## Known Limitations

- Dataset covers September 2018 – September 2020, including the COVID period
  (March–September 2020). Churn threshold calculated on pre-COVID transactions only.
- Sample covers 17% of total customers (~2.2 lakh). With full data, BG/NBD would
  be implemented alongside Cox PH for comparison.
- Price column is normalized (not raw GBP). All revenue figures are relative,
  not absolute currency amounts.

---

## Production Considerations

**Retraining triggers:** LTV model monthly. Cox model when observed churn rate
deviates from predicted by more than 5 percentage points.

**Monitoring:** Weekly predicted vs actual churn rate per segment.
Monthly ECE recalculation on new data.

**With more time:** dbt for SQL layer, Prefect for orchestration, MLflow for
model versioning.