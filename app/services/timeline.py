"""Timeline reconstruction service"""
from typing import List, Dict
from datetime import datetime

def build_timeline(drift_results: List[Dict], impact_results: List[Dict]) -> Dict:
    """
    Build failure timeline by correlating drift and impact
    
    This creates a chronological story of what went wrong
    
    Args:
        drift_results: Results from drift detection
        impact_results: Results from impact analysis
        
    Returns:
        Timeline dict with events and analysis
    """
    timeline = {
        "events": [],
        "summary": {},
        "critical_features": [],
        "recommendations": []
    }
    
    # Event 1: Identify drifted features
    drifted_features = [d for d in drift_results if d.get("drift", False)]
    
    if drifted_features:
        timeline["events"].append({
            "event_type": "drift_detected",
            "severity": "critical" if len(drifted_features) > 5 else "moderate",
            "description": f"Drift detected in {len(drifted_features)} features",
            "features": [d["feature"] for d in drifted_features],
            "timestamp": "production_period"
        })
    
    # Event 2: Identify high-impact features
    high_impact = [i for i in impact_results if i.get("impact_level") == "High"]
    
    if high_impact:
        timeline["events"].append({
            "event_type": "high_impact_detected",
            "severity": "critical",
            "description": f"{len(high_impact)} high-impact features identified",
            "features": [i["feature"] for i in high_impact],
            "timestamp": "analysis_time"
        })
    
    # Event 3: Correlate drift + impact (critical features)
    drifted_feature_names = set(d["feature"] for d in drifted_features)
    impact_feature_names = set(i["feature"] for i in high_impact)
    
    critical_features = list(drifted_feature_names & impact_feature_names)
    
    if critical_features:
        timeline["critical_features"] = critical_features
        timeline["events"].append({
            "event_type": "root_cause_identified",
            "severity": "critical",
            "description": f"Root cause likely: {', '.join(critical_features[:3])}",
            "features": critical_features,
            "timestamp": "correlation_analysis",
            "explanation": "These features both drifted AND have high impact on predictions"
        })
    
    # Generate summary
    timeline["summary"] = {
        "total_features_analyzed": len(drift_results),
        "drifted_features": len(drifted_features),
        "high_impact_features": len(high_impact),
        "critical_features": len(critical_features),
        "severity_assessment": _assess_overall_severity(drifted_features, high_impact, critical_features)
    }
    
    # Generate recommendations
    timeline["recommendations"] = _generate_timeline_recommendations(
        drifted_features, high_impact, critical_features
    )
    
    return timeline


def _assess_overall_severity(drifted, high_impact, critical) -> str:
    """Assess overall failure severity"""
    if len(critical) >= 3:
        return "CRITICAL - Immediate action required"
    elif len(critical) >= 1 or len(high_impact) >= 5:
        return "HIGH - Action recommended soon"
    elif len(drifted) >= 5:
        return "MODERATE - Monitor closely"
    else:
        return "LOW - Routine monitoring"


def _generate_timeline_recommendations(drifted, high_impact, critical) -> List[str]:
    """Generate actionable recommendations based on timeline"""
    recommendations = []
    
    if critical:
        # critical is a list of feature names (strings), not dictionaries
        feature_names = critical[:3] if isinstance(critical[0], str) else [f['feature'] for f in critical[:3]]
        recommendations.append(
            f"🚨 PRIORITY: Retrain model with recent data focusing on: {', '.join(feature_names)}"
        )
        recommendations.append(
            f"🔍 Investigate data pipeline for: {', '.join(feature_names)}"
        )
    
    # Check for new categorical values
    for feature in drifted:
        if feature.get("statistics", {}).get("new_categories"):
            new_cats = feature["statistics"]["new_categories"]
            recommendations.append(
                f"⚠️ Handle new categorical values in '{feature['feature']}': {new_cats}"
            )
    
    # Check for severe distribution shifts
    severe_drifts = [d for d in drifted if d.get("severity") == "High"]
    if severe_drifts:
        recommendations.append(
            f"📊 Severe distribution shifts detected in {len(severe_drifts)} features - consider feature engineering"
        )
    
    if len(recommendations) == 0:
        recommendations.append("✅ No critical issues detected - continue monitoring")
    
    return recommendations


def build_temporal_timeline(snapshots: List[Dict]) -> Dict:
    """
    Build timeline from multiple temporal snapshots
    
    This is the WOW factor - showing WHEN drift started
    
    Args:
        snapshots: List of {"timestamp": str, "data": DataFrame}
        
    Returns:
        Temporal timeline showing drift progression
    """
    temporal_timeline = {
        "snapshots": [],
        "drift_progression": {},
        "first_drift_detected": None,
        "acceleration_points": []
    }
    
    # This would be populated with actual drift detection across time
    # For MVP, we return the structure
    
    return temporal_timeline
