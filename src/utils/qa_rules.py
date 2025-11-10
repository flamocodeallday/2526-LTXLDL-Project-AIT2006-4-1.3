import pandas as pd
import numpy as np

'''
    This function returns a mask pandas Dataframe of all values in 1 month data, 1 is violated the rule, 0 is otherwise.

'''
def run_quality_check(df: pd.DataFrame) -> pd.DataFrame:
    qa_flags = pd.DataFrame(index=df.index)

    # Rule 1: Duplicated rows -> Action: Exclude
    qa_flags['is_duplicate'] = df.duplicated()

    # Rule 2: drop off before pick up -> Action: Exclude
    qa_flags['invalid_time_order'] = df["tpep_dropoff_datetime"] < df["tpep_pickup_datetime"]

    # Rule 3: Duration is negative -> Action: Exclude
    qa_flags['invalid_duration'] = df['trip_duration_minutes'] <= 0

    # Rule 4: Distance is negative -> Action: Exclude 
    qa_flags['invalid_distance'] = df["trip_distance"] <= 0

    # Rule 5: Speed is negative -> Action: Exclude
    qa_flags['invalid_speed'] = df['avg_speed_mph'] <= 0

    # Rule 6: Negative fare amount -> Action: Flag
    qa_flags['invalid_fare_amount'] = df['fare_amount'] <= 0

    # Rule 7: Negative tip amount -> Action: Flag
    qa_flags['invalid_tip_amount'] = df['tip_amount'] < 0

    # Rule 8: Negative total amount -> Action: Flag
    qa_flags['invalid_total_amount'] = df['total_amount'] <= 0

    # Rule 9: Invalid payment type (not in range [0,6]) -> Action: Flag
    qa_flags['invalid_payment_type'] = (df['payment_type'] < 0) | (df['payment_type'] > 6)

    # Rule 10 Invalid passenger counts -> Action: Flag
    qa_flags['invalid_passenger_count'] = df['passenger_count'] == 0

    # Rule 11: Zone ID does not exist -> Action: Flag
    qa_flags['invalid_zone'] = df[['PU_Borough', 'PU_Zone', 'DO_Borough', 'DO_Zone']].isna().any(axis = 1)

    return qa_flags

'''
    This function summarizes qa_flags into a pandas Series (format: "count/pct%").
    - The first 11 entries summarize violations for each individual rule.
    - The 12th entry (Total) summarizes the count of *unique trips* (rows) 
    that violated *at least one* rule.
'''
def summarize_qa_flags(qa_flags: pd.DataFrame) -> pd.Series:

    total_records = len(qa_flags)
    
    # Violations per rule
    violations_per_rule = qa_flags.sum()
    
    # Percentage of each in total
    percent_per_rule = (violations_per_rule / total_records * 100).round(2)
    
    # Create a result list
    final_list = []
    for rule_name in violations_per_rule.index:
        count = violations_per_rule[rule_name]
        pct = percent_per_rule[rule_name]
        final_list.append(f"{count}/{pct}%")

    # Count all row that has violations
    total_violated_rows = qa_flags.any(axis=1).sum()
    total_violated_percent = (total_violated_rows / total_records * 100).round(3)
    total_string = f"{total_violated_rows}/{total_violated_percent}%"
    
    final_list.append(total_string)
    return pd.Series(final_list)