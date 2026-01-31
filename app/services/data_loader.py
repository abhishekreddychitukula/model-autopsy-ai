"""Data loading and validation service"""
import pandas as pd
from typing import Tuple
from fastapi import UploadFile
import io

def normalize_columns(df):
    """Normalize column names to prevent hidden whitespace/case issues"""
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
    )
    return df


async def load_and_validate(
    train: UploadFile, 
    old: UploadFile, 
    new: UploadFile
) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Load and validate CSV files for autopsy analysis
    
    Args:
        train: Training data (baseline)
        old: Production data before failure
        new: Production data after failure
        
    Returns:
        Tuple of three DataFrames (train_df, old_df, new_df)
        
    Raises:
        ValueError: If validation fails
    """
    try:
        # Read file contents asynchronously
        train_content = await train.read()
        old_content = await old.read()
        new_content = await new.read()
        
        # Parse CSV from bytes
        train_df = pd.read_csv(io.BytesIO(train_content))
        old_df = pd.read_csv(io.BytesIO(old_content))
        new_df = pd.read_csv(io.BytesIO(new_content))
    except Exception as e:
        raise ValueError(f"CSV parsing failed: {str(e)}")

    # Normalize columns to handle whitespace and case issues
    train_df = normalize_columns(train_df)
    old_df = normalize_columns(old_df)
    new_df = normalize_columns(new_df)

    train_cols = set(train_df.columns)
    old_cols = set(old_df.columns)
    new_cols = set(new_df.columns)

    # Check that all files have the same columns (order doesn't matter)
    if train_cols != old_cols or train_cols != new_cols:
        missing_in_old = train_cols - old_cols
        missing_in_new = train_cols - new_cols
        extra_in_old = old_cols - train_cols
        extra_in_new = new_cols - train_cols
        
        error_msg = "Column mismatch detected.\n"
        if missing_in_old:
            error_msg += f"Missing in prod_old: {missing_in_old}\n"
        if missing_in_new:
            error_msg += f"Missing in prod_new: {missing_in_new}\n"
        if extra_in_old:
            error_msg += f"Extra in prod_old: {extra_in_old}\n"
        if extra_in_new:
            error_msg += f"Extra in prod_new: {extra_in_new}\n"
        
        raise ValueError(error_msg.strip())
    
    # Reorder columns to match training data for consistency
    train_col_order = list(train_df.columns)
    old_df = old_df[train_col_order]
    new_df = new_df[train_col_order]

    # Validation: Check for empty dataframes
    if train_df.empty or old_df.empty or new_df.empty:
        raise ValueError("One or more dataframes are empty")
    
    # Detect new categorical values (important for model failure analysis)
    new_values_detected = {}
    
    for col in train_df.columns:
        if train_df[col].dtype == 'object':
            train_unique = set(train_df[col].dropna().unique())
            new_unique = set(new_df[col].dropna().unique())
            
            new_vals = new_unique - train_unique
            if new_vals:
                new_values_detected[col] = list(new_vals)
    
    # Warning about new categorical values (not blocking, but important)
    if new_values_detected:
        print(f"⚠️ WARNING: New categorical values detected: {new_values_detected}")
    
    return train_df, old_df, new_df


def validate_predictions(predictions_file: UploadFile) -> pd.DataFrame:
    """
    Validate and load predictions CSV for SHAP analysis
    
    Expected columns: prediction, actual (optional), timestamp (optional)
    """
    try:
        pred_df = pd.read_csv(predictions_file.file)
        
        if 'prediction' not in pred_df.columns:
            raise ValueError("Predictions file must contain 'prediction' column")
        
        return pred_df
    except Exception as e:
        raise ValueError(f"Failed to load predictions: {str(e)}")
