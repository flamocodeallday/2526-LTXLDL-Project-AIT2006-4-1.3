# src/

This directory contains reusable Python modules that support data processing, analysis, and modeling tasks used throughout the project notebooks.

The scripts in this folder are designed as utility functions (helpers) to keep notebooks clean, modular, and easier to maintain.

---

## Overview

- All modules in `src/` are imported and executed from Jupyter notebooks
- No scripts are intended to be run as standalone programs
- Functions are organized by responsibility (cleaning, QA, KPIs, forecasting, clustering, etc.)

---

## Module Descriptions

### cleaning.py
- Handle initial data cleaning steps
- Remove invalid records and apply basic data filters
- Standardize datetime formats and essential columns

### normalizing.py
- Normalize and standardize numerical variables
- Prepare features for downstream analysis and modeling

### qa_rules.py
- Define data quality and validation rules
- Generate QA flags for anomaly detection and filtering
- Support reproducible data quality checks

### kpi.py
- Compute key performance indicators (KPIs) related to trips
- Support zone-level and time-based aggregations
- Used as inputs for analysis and clustering

### forecasting.py
- Aggregate trip data by time (hourly / daily)
- Apply time-series forecasting methods
- Evaluate forecasts using metrics such as MAE, MAPE, and RMSE
- Provide baseline and model-based predictions

### cluster_zone.py
- Perform clustering on taxi zones using KPI-based features
- Apply scaling and clustering algorithms
- Assign interpretable labels to clusters for analysis

### visualization.py
- Generate reusable plotting functions
- Support consistent visualization styles across notebooks
- Used for EDA, KPI visualization, and result interpretation

---

## Usage

Modules in this directory are imported into notebooks as needed.  
Example:

```python
from src.forecasting import forecast_and_evaluate
from src.cluster_zone import cluster_zones_with_kpi
