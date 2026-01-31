"""Statistical utility functions"""
import numpy as np
import pandas as pd
from typing import Union

def calculate_psi(baseline: pd.Series, current: pd.Series, bins: int = 10) -> float:
    """
    Calculate Population Stability Index (PSI)
    
    PSI measures distribution shift for categorical or binned numerical data
    
    Formula:
    PSI = Σ (actual% - expected%) * ln(actual% / expected%)
    
    Interpretation:
    - PSI < 0.1: No significant change
    - 0.1 ≤ PSI < 0.25: Moderate change
    - PSI ≥ 0.25: Significant change (retrain recommended)
    
    Args:
        baseline: Expected distribution (training data)
        current: Actual distribution (production data)
        bins: Number of bins for numerical data
        
    Returns:
        PSI value
    """
    # Determine if data is categorical or numerical
    is_categorical = (
        pd.api.types.is_object_dtype(baseline) or 
        pd.api.types.is_categorical_dtype(baseline) or
        pd.api.types.is_string_dtype(baseline) or
        pd.api.types.is_object_dtype(current) or 
        pd.api.types.is_categorical_dtype(current) or
        pd.api.types.is_string_dtype(current)
    )
    
    # Handle categorical data
    if is_categorical:
        # Get value counts as proportions
        baseline_dist = baseline.value_counts(normalize=True, dropna=False)
        current_dist = current.value_counts(normalize=True, dropna=False)
        
        # Align both distributions
        all_categories = set(baseline_dist.index) | set(current_dist.index)
        
        psi = 0
        for category in all_categories:
            expected_pct = baseline_dist.get(category, 0.0001)  # Small value to avoid log(0)
            actual_pct = current_dist.get(category, 0.0001)
            
            # Ensure no zero values
            if expected_pct == 0:
                expected_pct = 0.0001
            if actual_pct == 0:
                actual_pct = 0.0001
            
            psi += (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
        
        return psi
    
    # Handle numerical data - bin it first
    else:
        # Create bins based on baseline distribution
        baseline_clean = baseline.dropna()
        current_clean = current.dropna()
        
        if len(baseline_clean) == 0 or len(current_clean) == 0:
            return 0.0
        
        # Create quantile-based bins
        _, bin_edges = pd.qcut(baseline_clean, q=bins, retbins=True, duplicates='drop')
        
        # Bin both distributions
        baseline_binned = pd.cut(baseline_clean, bins=bin_edges, include_lowest=True)
        current_binned = pd.cut(current_clean, bins=bin_edges, include_lowest=True)
        
        # Get proportions
        baseline_dist = baseline_binned.value_counts(normalize=True, dropna=False)
        current_dist = current_binned.value_counts(normalize=True, dropna=False)
        
        # Calculate PSI
        psi = 0
        all_bins = set(baseline_dist.index) | set(current_dist.index)
        
        for bin_val in all_bins:
            expected_pct = baseline_dist.get(bin_val, 0.0001)
            actual_pct = current_dist.get(bin_val, 0.0001)
            
            if expected_pct == 0:
                expected_pct = 0.0001
            if actual_pct == 0:
                actual_pct = 0.0001
            
            psi += (actual_pct - expected_pct) * np.log(actual_pct / expected_pct)
        
        return psi


def get_severity_level(score: float, method: str = "ks") -> str:
    """
    Convert drift score to severity level
    
    Args:
        score: Drift score (KS statistic, PSI, etc.)
        method: Detection method ('ks', 'psi')
        
    Returns:
        Severity level: 'None', 'Low', 'Moderate', 'High'
    """
    if method == "ks":
        # KS statistic ranges from 0 to 1
        if score < 0.1:
            return "None"
        elif score < 0.2:
            return "Low"
        elif score < 0.3:
            return "Moderate"
        else:
            return "High"
    
    elif method == "psi":
        # PSI thresholds
        if score < 0.1:
            return "None"
        elif score < 0.25:
            return "Moderate"
        else:
            return "High"
    
    return "Unknown"


def calculate_wasserstein_distance(baseline: pd.Series, current: pd.Series) -> float:
    """
    Calculate Wasserstein distance (Earth Mover's Distance)
    
    Useful for numerical distributions - measures "effort" to transform one distribution to another
    """
    from scipy.stats import wasserstein_distance
    
    baseline_clean = baseline.dropna()
    current_clean = current.dropna()
    
    if len(baseline_clean) == 0 or len(current_clean) == 0:
        return 0.0
    
    return wasserstein_distance(baseline_clean, current_clean)


def calculate_jensen_shannon_divergence(baseline: pd.Series, current: pd.Series) -> float:
    """
    Calculate Jensen-Shannon Divergence
    
    Symmetric measure of distribution similarity (range: 0 to 1)
    """
    from scipy.spatial.distance import jensenshannon
    
    # Get probability distributions
    baseline_dist = baseline.value_counts(normalize=True, dropna=False).sort_index()
    current_dist = current.value_counts(normalize=True, dropna=False).sort_index()
    
    # Align indices
    all_vals = sorted(set(baseline_dist.index) | set(current_dist.index))
    
    p = np.array([baseline_dist.get(v, 0) for v in all_vals])
    q = np.array([current_dist.get(v, 0) for v in all_vals])
    
    # Add small epsilon to avoid log(0)
    p = p + 1e-10
    q = q + 1e-10
    
    # Normalize
    p = p / p.sum()
    q = q / q.sum()
    
    return jensenshannon(p, q)
