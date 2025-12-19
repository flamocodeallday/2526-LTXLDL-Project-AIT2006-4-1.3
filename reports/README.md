# reports/

This directory stores generated reports and summary outputs produced during data quality checks, KPI computation, and zone-level clustering.

All files and subfolders in this directory are created automatically by the analysis pipelines and notebooks.

---

## Contents

### QA Reports
- `qa_summary.csv`  
  Summary of data quality checks and validation rules applied to the raw and processed datasets.

### KPI Reports
- `kpi_daily_2021.csv`  
  Daily aggregated KPIs for taxi trips in 2021.

- `kpi_weekly_2021.csv`  
  Weekly aggregated KPIs derived from cleaned trip data.

- `kpi_montly_2021.csv`  
  Monthly aggregated KPIs summarizing long-term trends.  

### Clustering Reports
- `cluster_zone/`  
  Contains zone-level clustering outputs and related summaries.
  Subfolders and files are generated automatically during clustering analysis.

---

## Notes

- This directory contains **generated outputs only**
- Files should not be manually edited
- Existing files may be overwritten when the analysis is re-run
- Subfolders are created dynamically during execution

---

## Reproducibility

To reproduce the contents of this directory:
1. Ensure raw and processed data are available
2. Run the notebooks in the recommended order
3. All reports will be regenerated automatically
