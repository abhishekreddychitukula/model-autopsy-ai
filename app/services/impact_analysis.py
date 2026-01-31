"""Feature impact analysis service"""
import pandas as pd
import numpy as np
from typing import List, Dict, Optional

def analyze_impact(
    train_df: pd.DataFrame, 
    old_df: pd.DataFrame, 
    new_df: pd.DataFrame,
    model=None,
    predictions_df: Optional[pd.DataFrame] = None
) -> List[Dict]:
    """
    Analyze the impact of drifted features on model performance
    
    Two approaches:
    1. If model available: Use SHAP values (best)
    2. If model not available: Use proxy metrics (hackathon-safe)
    
    Args:
        train_df: Training data
        old_df: Production data before failure
        new_df: Production data after failure
        model: Optional trained model for SHAP analysis
        predictions_df: Optional predictions for error correlation
        
    Returns:
        List of feature impact scores
    """
    impact_results = []
    
    # Approach 1: Proxy impact (works without model)
    for col in train_df.columns:
        if train_df[col].dtype in ['int64', 'float64', 'int32', 'float32']:
            impact = _calculate_proxy_impact(train_df[col], old_df[col], new_df[col], col)
        else:
            impact = _calculate_categorical_impact(train_df[col], old_df[col], new_df[col], col)
        
        impact_results.append(impact)
    
    # Sort by impact score
    impact_results.sort(key=lambda x: x['impact_score'], reverse=True)
    
    return impact_results


def _calculate_proxy_impact(
    train_series: pd.Series,
    old_series: pd.Series, 
    new_series: pd.Series,
    feature_name: str
) -> Dict:
    """
    Calculate proxy impact for numerical features
    
    Metrics:
    - Mean shift magnitude
    - Standard deviation change
    - Distribution overlap reduction
    """
    train_clean = train_series.dropna()
    old_clean = old_series.dropna()
    new_clean = new_series.dropna()
    
    if len(train_clean) == 0 or len(new_clean) == 0:
        return {
            "feature": feature_name,
            "impact_score": 0,
            "impact_level": "None",
            "reason": "Insufficient data"
        }
    
    # Calculate mean shift
    train_mean = train_clean.mean()
    new_mean = new_clean.mean()
    mean_shift = abs(new_mean - train_mean) / (abs(train_mean) + 1e-10)
    
    # Calculate variance change
    train_std = train_clean.std()
    new_std = new_clean.std()
    variance_change = abs(new_std - train_std) / (abs(train_std) + 1e-10)
    
    # Calculate distribution overlap (simplified)
    train_range = (train_clean.min(), train_clean.max())
    new_range = (new_clean.min(), new_clean.max())
    
    overlap = _calculate_range_overlap(train_range, new_range)
    overlap_loss = 1 - overlap
    
    # Combined impact score (weighted)
    impact_score = (
        0.4 * mean_shift + 
        0.3 * variance_change + 
        0.3 * overlap_loss
    )
    
    # Determine impact level
    if impact_score < 0.1:
        impact_level = "Low"
    elif impact_score < 0.3:
        impact_level = "Moderate"
    else:
        impact_level = "High"
    
    return {
        "feature": feature_name,
        "impact_score": round(impact_score, 4),
        "impact_level": impact_level,
        "metrics": {
            "mean_shift": round(mean_shift, 4),
            "variance_change": round(variance_change, 4),
            "distribution_overlap_loss": round(overlap_loss, 4)
        },
        "statistics": {
            "train_mean": round(train_mean, 4),
            "old_mean": round(old_clean.mean(), 4),
            "new_mean": round(new_mean, 4),
            "trend": "increasing" if new_mean > train_mean else "decreasing"
        }
    }


def _calculate_categorical_impact(
    train_series: pd.Series,
    old_series: pd.Series,
    new_series: pd.Series,
    feature_name: str
) -> Dict:
    """
    Calculate impact for categorical features
    
    Metrics:
    - Category distribution shift
    - New categories introduced
    - Rare category emergence
    """
    train_clean = train_series.dropna()
    new_clean = new_series.dropna()
    
    if len(train_clean) == 0 or len(new_clean) == 0:
        return {
            "feature": feature_name,
            "impact_score": 0,
            "impact_level": "None",
            "reason": "Insufficient data"
        }
    
    # Get distributions
    train_dist = train_clean.value_counts(normalize=True)
    new_dist = new_clean.value_counts(normalize=True)
    
    # Calculate category changes
    train_categories = set(train_dist.index)
    new_categories = set(new_dist.index)
    
    newly_appeared = new_categories - train_categories
    disappeared = train_categories - new_categories
    
    # Calculate distribution shift (total variation distance)
    all_categories = train_categories | new_categories
    tvd = 0
    for cat in all_categories:
        train_prob = train_dist.get(cat, 0)
        new_prob = new_dist.get(cat, 0)
        tvd += abs(new_prob - train_prob)
    
    tvd = tvd / 2  # Normalize
    
    # Impact score considers both new categories and distribution shift
    new_cat_penalty = len(newly_appeared) * 0.1
    impact_score = tvd + new_cat_penalty
    
    # Determine impact level
    if impact_score < 0.2:
        impact_level = "Low"
    elif impact_score < 0.4:
        impact_level = "Moderate"
    else:
        impact_level = "High"
    
    return {
        "feature": feature_name,
        "impact_score": round(impact_score, 4),
        "impact_level": impact_level,
        "metrics": {
            "distribution_shift": round(tvd, 4),
            "new_categories_count": len(newly_appeared),
            "disappeared_categories_count": len(disappeared)
        },
        "statistics": {
            "new_categories": list(newly_appeared)[:5] if newly_appeared else None,
            "disappeared_categories": list(disappeared)[:5] if disappeared else None,
            "top_train_category": train_dist.index[0] if len(train_dist) > 0 else None,
            "top_new_category": new_dist.index[0] if len(new_dist) > 0 else None
        }
    }


def _calculate_range_overlap(range1, range2):
    """Calculate overlap ratio between two ranges"""
    min1, max1 = range1
    min2, max2 = range2
    
    overlap_start = max(min1, min2)
    overlap_end = min(max1, max2)
    
    if overlap_start >= overlap_end:
        return 0.0
    
    overlap_length = overlap_end - overlap_start
    total_range = max(max1, max2) - min(min1, min2)
    
    if total_range == 0:
        return 1.0
    
    return overlap_length / total_range


def calculate_shap_impact(model, train_df: pd.DataFrame, new_df: pd.DataFrame) -> List[Dict]:
    """
    Calculate feature importance using SHAP values (advanced version)
    
    Use this when model is available for more accurate impact analysis
    """
    import shap
    
    # Create explainer
    explainer = shap.Explainer(model, train_df)
    
    # Calculate SHAP values for production data
    shap_values = explainer(new_df)
    
    # Get mean absolute SHAP values per feature
    feature_importance = np.abs(shap_values.values).mean(axis=0)
    
    results = []
    for idx, col in enumerate(train_df.columns):
        results.append({
            "feature": col,
            "shap_importance": round(feature_importance[idx], 4),
            "method": "SHAP"
        })
    
    results.sort(key=lambda x: x['shap_importance'], reverse=True)
    
    return results
