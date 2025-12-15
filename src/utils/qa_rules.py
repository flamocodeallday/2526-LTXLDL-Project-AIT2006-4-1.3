import pandas as pd
import numpy as np

'''
    This function returns a mask pandas Dataframe of all values in 1 month data, 1 is violated the rule, 0 is otherwise.

'''
def run_quality_check(df: pd.DataFrame, current_month: int) -> pd.DataFrame:
    qa_flags = pd.DataFrame(index=df.index)
    
    # Rule 1: Duplicated rows -> Action: Exclude
    qa_flags['is_duplicate'] = df.duplicated()

    # RULES RELATED TO DATETIME AND TRIP LOGIC
    # Rule 2: Missing pickup or dropoff datetime -> Action: Exclude
    qa_flags['missing_datetime'] = df['tpep_pickup_datetime'].isna() | df['tpep_dropoff_datetime'].isna()

    # Rule 3: Drop off before pick up -> Action: Exclude
    qa_flags['invalid_time_order'] = df["tpep_dropoff_datetime"] < df["tpep_pickup_datetime"]

    # Rule 4: Invalid month, year -> Action: Exclude 
    qa_flags['invalid_month'] = (df['tpep_pickup_datetime'].dt.month != current_month) | (df['tpep_pickup_datetime'].dt.year != 2021)

    # RULES RELATED TO TRIP FEATURES
    # Rule 5: Duration is negative -> Action: Exclude
    qa_flags['invalid_duration'] = df['trip_duration_minutes'] <= 0

    # Rule 6: Distance is negative -> Action: Exclude 
    qa_flags['invalid_distance'] = df["trip_distance"] <= 0

    # Rule 7: Speed is negative -> Action: Exclude
    qa_flags['invalid_speed'] = df['avg_speed_mph'] <= 0

    # Rule 8: Zero fare but distance > 0 -> Action: Flag (suspicious)
    qa_flags['suspicious_zero_fare'] = (df['fare_amount'] == 0) & (df['trip_distance'] > 0)

    # Rule 9: Very short duration but nontrivial distance -> Action: Flag
    qa_flags['short_duration_long_distance'] = (df['trip_duration_minutes'] < 1) & (df['trip_distance'] > 1)

    # Rule 10: Excessive average speed -> Action: Flag
    qa_flags['excessive_speed'] = df['avg_speed_mph'] > 66

    # Rule 11: Excessive duration (more than 24 hours) -> Action: Flag
    qa_flags['excessive_duration'] = df['trip_duration_minutes'] > (24 * 60)

    # RULES RELATED TO PAYMENT AND AMOUNTS
    # Rule 12: Negative fare amount -> Action: Flag
    qa_flags['invalid_fare_amount'] = df['fare_amount'] <= 0

    # Rule 13: Negative tip amount -> Action: Flag
    qa_flags['invalid_tip_amount'] = df['tip_amount'] < 0
    
    # Rule 14: Negative extra amount -> Action: Flag
    qa_flags['invalid_extra'] = df['extra'] < 0

    # Rule 15: Negative tolls amount -> Action: Flag
    qa_flags['invalid_tolls_amount'] = df['tolls_amount'] < 0

    # Rule 16: Negative total amount -> Action: Flag
    qa_flags['invalid_total_amount'] = df['total_amount'] <= 0

    # Rule 17: Fare/amount arithmetic mismatch -> Action: Flag
    qa_flags['fare_total_mismatch'] = (df['total_amount'].fillna(0) - df['computed_total_amount']).abs() > 1.0

    # Rule 18: Invalid payment type (not in range [0,6]) -> Action: Flag
    qa_flags['invalid_payment_type'] = (df['payment_type'] < 0) | (df['payment_type'] > 6)

    # Rule 19: Invalid RatecodeID -> Action: Flag
    qa_flags['invalid_ratecode'] = ~df['RatecodeID'].isin([1,2,3,4,5,6,99])

    # Rule 20: Unusual passenger counts -> Action: Flag
    qa_flags['unusual_passenger_count'] = (df['passenger_count'] == 0 ) | (df['passenger_count'] > 5)

    # Rule 21: Zone ID does not exist -> Action: Flag
    qa_flags['invalid_zone'] = df[['PU_Borough', 'PU_Zone', 'DO_Borough', 'DO_Zone']].isna().any(axis = 1)

    return qa_flags

'''
    This function summarizes qa_flags into a pandas Series (format: "count/pct%").
    - The first 22 entries summarize violations for each individual rule.
    - The 23th entry (Total) summarizes the count of *unique trips* (rows) 
    that violated *at least one* rule.
'''
def summarize_qa_flags(qa_flags: pd.DataFrame):

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

    # Calulate threshold for garbage rows
    qa_flags['total_violations'] = qa_flags.sum(axis=1)
    threshold = qa_flags['total_violations'].quantile(0.95).astype(int)
    return pd.Series(final_list), threshold