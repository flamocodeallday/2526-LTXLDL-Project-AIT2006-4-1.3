# 2526-LTXLDL-Project-AIT2006-4-1.3
A Python project for cleaning, normalizing, and aggregating NYC TLC taxi trip data

## Project Information
- Course: AIT2006 – Data Analysis Programming
- Academic Year: 2025–2026
- Dataset: NYC TLC Yellow Taxi Trip Records (2021)
- Project Type: Group Project
- Members: Phạm Quang Minh, Phạm Nguyễn Xuân Tùng, Phạm Vũ Nam

## Introduction
This project focuses on processing and analyzing the NYC Taxi & Limousine Commission (TLC) Yellow Taxi Trip Data. The dataset contains millions of taxi trip records with information related to pickup and drop-off times, locations, trip distance, fares, and tips.

The main goal of the project is to transform raw, large-scale taxi trip data into clean, structured, and meaningful datasets that can be used for exploratory data analysis (EDA), KPI calculation, and visualization. The project also emphasizes reproducibility, clear project structure, and good data engineering practices.

## Objectives
- Clean and preprocess raw NYC TLC Yellow Taxi trip data
- Handle missing values, invalid records, and outliers
- Normalize time, distance, and fare-related variables
- Aggregate trip data by time, location, and administrative levels (e.g., borough)
- Generate key performance indicators (KPIs) for analysis
- Support reproducible analysis through a well-defined environment and structure
- Forecast taxi trip demand using baseline methods, ARIMA, and linear regression models
- Cluster taxi zones by time-of-day using KPI-based features to identify demand and traffic patterns


## Project Structure
```text
2526-LTXLDL-Project-AIT2006-4-1.3/
│
├── figures/                # Monthly figures 
│   ├── January_figures     # Monthly subfolders are created automatically during analysis
│   ├── Febuary_figures
│   ├── ...
│   ├── December_figures             
│   └── 2021
│
├── notebooks/              # Jupyter notebooks for analysis
│   ├── 1_view_data.ipynb
│   ├── 2_normalize_clean.ipynb
│   ├── 3_analysis.ipynb
│   └── 4_advanced.ipynb
│
├── processed/          
│   ├── cleaned_data        # Cleaned and normalized datasets
│   └── flags_for_analysis  # QA flags for analysis
│
├── raw/                    # Original NYC TLC data files and taxi lookup zone table
│
├── reports/                # QA summary, kpi reports and cluster zone reports, all subfolders are created automatically
│   ├── cluster_zone
│   ├── kpi_daily_2021.csv
│   ├── kpi_montly_2021.csv
│   ├── kpi_weekly_2021.csv
│   └── qa_summary.csv
│   
├── src/                    # Python source code
│   ├── __init__.py
│   ├── cleaning.py
│   ├── cluster_zone.py
│   ├── forecasting.py
│   ├── kpi.py
│   ├── normalizing.py
│   ├── qa_rules.py
│   ├── visualization.py
│   └── kpi.py
│
├── .gitignore
├── README.md
└── requirements.txt

```

## Requirements
- Python 3.9 or higher
- Operating System: Windows, macOS, or Linux

### Main Python Libraries
- pandas
- numpy
- matplotlib
- seaborn
- sklearn

## Environment setup
This project does not use environment variables.
All paths and configurations are defined directly within the code.

## How to run the Project
1. Download NYC TLC Yellow Taxi trip data 2021, including 12 months parquet files and a csv taxi look up zone file at [Official TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
2. Place all raw data files in the `raw` directory. The directory should contain files such as `yellow_tripdata_2021-01.parquet` and `taxi_zone_lookup.csv`
3. Activate the virtual environment, install requirements
4. Run the notebooks in order:
- `1_view_data.ipynb`
- `2_normalize_clean.ipynb`
- `3_analysis.ipynb`
- `4_advanced.ipynb`

## Notes
- This project is intended for educational and research purposes
- The dataset is provided by the NYC Taxi & Limousine Commission (TLC)
- Results and interpretations are subject to data quality and preprocessing assumptions
