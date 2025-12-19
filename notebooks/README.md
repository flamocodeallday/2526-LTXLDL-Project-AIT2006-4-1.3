# Notebooks

This directory contains Jupyter notebooks used for data exploration, preprocessing, analysis, and advanced modeling.

The notebooks are designed to be executed sequentially to ensure correct data dependencies and reproducibility.

---

## Notebook Overview

### 1_view_data.ipynb
- Load and inspect raw NYC TLC taxi trip data
- Perform initial data exploration
- Review schema, data ranges, and basic statistics

### 2_normalize_clean.ipynb
- Clean and normalize raw trip data
- Apply data quality rules and generate QA flags
- Produce cleaned datasets and validation outputs

### 3_analysis.ipynb
- Conduct exploratory data analysis (EDA)
- Compute key performance indicators (KPIs)
- Generate summary tables and visualizations

### 4_advanced.ipynb
- Perform advanced analytical tasks
- Apply time-series forecasting techniques
- Conduct zone-level clustering and interpret results

---

## Execution Order

Notebooks should be run in the following order:

1. `1_view_data.ipynb`  
2. `2_normalize_clean.ipynb`  
3. `3_analysis.ipynb`  
4. `4_advanced.ipynb`

Running notebooks out of order may result in missing or inconsistent outputs.

---

## Notes

- Notebooks rely on utility functions defined in the `src/` directory
- Intermediate datasets and reports are saved automatically
- Notebooks are not intended to be executed in isolation

---

## Reproducibility

To reproduce all results:
1. Ensure raw data is available in `raw/`
2. Install required dependencies
3. Execute the notebooks in the specified order
