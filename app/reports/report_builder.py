"""Report builder - assembles final autopsy report"""
from typing import List, Dict
from datetime import datetime

def build_report(
    drift_results: List[Dict],
    impact_results: List[Dict],
    timeline: Dict,
    diagnosis: Dict
) -> Dict:
    """
    Build comprehensive autopsy report
    
    This is what gets returned to the user/dashboard
    
    Args:
        drift_results: Drift detection results
        impact_results: Impact analysis results
        timeline: Timeline analysis
        diagnosis: LLM diagnosis
        
    Returns:
        Complete autopsy report
    """
    
    report = {
        "metadata": {
            "report_type": "ML Model Autopsy",
            "generated_at": datetime.now().isoformat(),
            "version": "1.0.0",
            "status": "completed"
        },
        
        "executive_summary": {
            "summary": diagnosis.get("executive_summary", "Analysis completed"),
            "severity": diagnosis.get("severity_assessment", "Unknown"),
            "business_impact": diagnosis.get("business_impact", "Unknown"),
            "critical_features_count": timeline.get("summary", {}).get("critical_features", 0),
            "recommendation_priority": _get_priority_level(diagnosis)
        },
        
        "drift_analysis": {
            "summary": {
                "total_features_analyzed": len(drift_results),
                "drifted_features_count": sum(1 for d in drift_results if d.get("drift", False)),
                "severe_drift_count": sum(1 for d in drift_results if d.get("severity") == "High")
            },
            "drift_leaderboard": sorted(
                [d for d in drift_results if d.get("drift", False)],
                key=lambda x: x.get("drift_score", 0),
                reverse=True
            )[:10],  # Top 10 drifted features
            "all_results": drift_results
        },
        
        "impact_analysis": {
            "summary": {
                "high_impact_count": sum(1 for i in impact_results if i.get("impact_level") == "High"),
                "moderate_impact_count": sum(1 for i in impact_results if i.get("impact_level") == "Moderate"),
                "low_impact_count": sum(1 for i in impact_results if i.get("impact_level") == "Low")
            },
            "impact_leaderboard": sorted(
                impact_results,
                key=lambda x: x.get("impact_score", 0),
                reverse=True
            )[:10],  # Top 10 impactful features
            "all_results": impact_results
        },
        
        "timeline": timeline,
        
        "diagnosis": diagnosis,
        
        "recommendations": {
            "immediate_actions": diagnosis.get("technical_recommendations", [])[:5],
            "all_recommendations": timeline.get("recommendations", [])
        },
        
        "visualizations": {
            "drift_chart_data": _prepare_drift_chart_data(drift_results),
            "impact_chart_data": _prepare_impact_chart_data(impact_results),
            "correlation_data": _prepare_correlation_data(drift_results, impact_results)
        }
    }
    
    return report


def _get_priority_level(diagnosis: Dict) -> str:
    """Determine priority level from diagnosis"""
    severity = diagnosis.get("severity_assessment", "")
    
    if "CRITICAL" in severity:
        return "P0 - Critical"
    elif "HIGH" in severity:
        return "P1 - High"
    elif "MODERATE" in severity:
        return "P2 - Moderate"
    else:
        return "P3 - Low"


def _prepare_drift_chart_data(drift_results: List[Dict]) -> Dict:
    """Prepare data for drift visualization"""
    
    drifted = [d for d in drift_results if d.get("drift", False)]
    
    chart_data = {
        "type": "bar_chart",
        "title": "Drift Severity by Feature",
        "x_axis": [d["feature"] for d in drifted[:15]],  # Top 15
        "y_axis": [d.get("drift_score", 0) for d in drifted[:15]],
        "colors": [_get_severity_color(d.get("severity", "None")) for d in drifted[:15]]
    }
    
    return chart_data


def _prepare_impact_chart_data(impact_results: List[Dict]) -> Dict:
    """Prepare data for impact visualization"""
    
    top_impact = sorted(
        impact_results,
        key=lambda x: x.get("impact_score", 0),
        reverse=True
    )[:15]
    
    chart_data = {
        "type": "horizontal_bar",
        "title": "Feature Impact Scores",
        "y_axis": [i["feature"] for i in top_impact],
        "x_axis": [i.get("impact_score", 0) for i in top_impact],
        "colors": [_get_impact_color(i.get("impact_level", "Low")) for i in top_impact]
    }
    
    return chart_data


def _prepare_correlation_data(drift_results: List[Dict], impact_results: List[Dict]) -> Dict:
    """Prepare drift vs impact correlation data"""
    
    # Create feature map
    impact_map = {i["feature"]: i.get("impact_score", 0) for i in impact_results}
    
    correlation_points = []
    
    for drift in drift_results:
        if drift.get("drift", False):
            feature = drift["feature"]
            correlation_points.append({
                "feature": feature,
                "drift_score": drift.get("drift_score", 0),
                "impact_score": impact_map.get(feature, 0),
                "is_critical": drift.get("drift_score", 0) > 0.2 and impact_map.get(feature, 0) > 0.3
            })
    
    return {
        "type": "scatter_plot",
        "title": "Drift vs Impact Correlation",
        "x_label": "Drift Score",
        "y_label": "Impact Score",
        "points": correlation_points
    }


def _get_severity_color(severity: str) -> str:
    """Get color for severity level"""
    color_map = {
        "High": "#DC2626",      # Red
        "Moderate": "#F59E0B",  # Orange
        "Low": "#10B981",       # Green
        "None": "#6B7280"       # Gray
    }
    return color_map.get(severity, "#6B7280")


def _get_impact_color(impact_level: str) -> str:
    """Get color for impact level"""
    color_map = {
        "High": "#7C3AED",      # Purple
        "Moderate": "#3B82F6",  # Blue
        "Low": "#8B5CF6"        # Light purple
    }
    return color_map.get(impact_level, "#8B5CF6")


def generate_pdf_report(report: Dict) -> bytes:
    """
    Generate PDF version of report (optional enhancement)
    
    For hackathon: return JSON/HTML is sufficient
    """
    # TODO: Implement PDF generation using reportlab or similar
    pass


def generate_html_report(report: Dict) -> str:
    """
    Generate HTML version of report for email/viewing
    
    For hackathon: return JSON is sufficient
    """
    html = f"""
    <html>
    <head>
        <title>Model Autopsy Report</title>
        <style>
            body {{ font-family: Arial, sans-serif; margin: 40px; }}
            .critical {{ color: #DC2626; font-weight: bold; }}
            .moderate {{ color: #F59E0B; }}
            .low {{ color: #10B981; }}
            table {{ border-collapse: collapse; width: 100%; margin: 20px 0; }}
            th, td {{ border: 1px solid #ddd; padding: 12px; text-align: left; }}
            th {{ background-color: #4F46E5; color: white; }}
        </style>
    </head>
    <body>
        <h1>🔬 Model Autopsy Report</h1>
        <p><strong>Generated:</strong> {report['metadata']['generated_at']}</p>
        
        <h2>Executive Summary</h2>
        <p class="{report['executive_summary']['severity'].lower()}">{report['executive_summary']['summary']}</p>
        
        <h2>Drift Analysis</h2>
        <p>Features with drift: {report['drift_analysis']['summary']['drifted_features_count']}</p>
        
        <h2>Diagnosis</h2>
        <pre>{report['diagnosis'].get('full_diagnosis', 'N/A')}</pre>
    </body>
    </html>
    """
    return html
