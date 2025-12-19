# Raw Data

This directory contains the original, unprocessed datasets used in the project.  
All files in this folder are treated as read-only inputs for downstream processing.

---

## Contents

### Yellow Taxi Trip Data (Parquet)
- `yellow_tripdata_YYYY-MM.parquet`  
  Monthly NYC TLC Yellow Taxi trip records stored in Parquet format.

  These files include raw trip-level information such as:
  - Pickup and drop-off timestamps
  - Trip distance and duration
  - Fare and payment details
  - Pickup and drop-off location IDs

### Taxi Zone Lookup (CSV)
- `taxi_zone_lookup.csv`  
  Lookup table mapping location IDs to taxi zones, boroughs, and service areas.

  This file is used to:
  - Decode pickup and drop-off location IDs
  - Enable zone-level and borough-level analysis
  - Support spatial aggregation and clustering

---

## Data Source

- NYC Taxi & Limousine Commission (TLC)  
- Official open data provided by NYC TLC

---

## Notes

- Data in this directory is **not cleaned or validated**
- Files should not be modified manually
- All preprocessing and filtering are handled in downstream pipelines
- File naming conventions are expected to follow the official TLC format

---

## Usage

Raw data files are loaded by data cleaning and preprocessing scripts located in the `src/` directory and by notebooks in the `notebooks/` folder.
