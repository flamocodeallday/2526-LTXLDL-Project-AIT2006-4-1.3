# Processed Data

This directory contains intermediate datasets that have been cleaned, validated, and prepared for analysis.

All files in this folder are generated from the raw data through reproducible preprocessing pipelines.

---

## Directory Structure

### cleaned_data/
This subfolder stores cleaned and standardized datasets derived from the raw NYC TLC trip data.

Typical processing steps include:
- Removal of invalid or corrupted records
- Standardization of datetime formats
- Filtering based on data quality rules
- Feature engineering (e.g. trip duration, average speed)

The datasets in this folder are used directly for:
- Exploratory data analysis (EDA)
- KPI computation
- Forecasting and clustering tasks

### flags_for_analysis/
This subfolder contains data quality and validation flags generated during preprocessing.

These flags are used to:
- Identify anomalies and rule violations
- Support transparent data quality assessment
- Enable flexible filtering during analysis without modifying the cleaned data

Each flag dataset corresponds to specific QA rules defined in the preprocessing pipeline.

---

## Notes

- All contents in this directory are **auto-generated**
- Files may be overwritten when preprocessing is re-run
- Processed data should not be edited manually
- Raw data should always remain unchanged

---

## Reproducibility

To regenerate the processed datasets:
1. Place the original raw data in `raw/`
2. Run the data cleaning and QA notebooks or scripts
3. All processed outputs will be recreated in this directory
