import pandas as pd

"""
    Cleans the DataFrame based on the QA flags and a "garbage threshold".
"""
def clean(normalized: pd.DataFrame, qa_flags: pd.DataFrame, threshold: int = 5):
    # Rules to remove due to invalid values
    remove = ['is_duplicate', 'invalid_time_order', 'invalid_duration', 'invalid_distance', 'invalid_speed', 'invalid_month']

    # Identify rows that violates more than threshold columns
    qa_flags['total_violations'] = qa_flags.sum(axis=1)
    qa_flags['is_garbage_row'] = qa_flags['total_violations'] > threshold
    remove.append('is_garbage_row')

    # Create final exclusion mask
    mask_to_exclude = qa_flags[remove].any(axis = 1)
    mask_to_keep = ~mask_to_exclude

    # Filter the normalized data, also return the standard mask for upcoming analysis
    cleaned = normalized[mask_to_keep].copy()
    standard = qa_flags[mask_to_keep].copy()

    return cleaned, standard