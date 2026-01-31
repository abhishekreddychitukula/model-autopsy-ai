"""LLM-powered diagnosis engine"""
import os
import json
from typing import List, Dict
from app.config import OPENAI_API_KEY

def generate_diagnosis(
    drift_results: List[Dict],
    impact_results: List[Dict],
    timeline: Dict
) -> Dict:
    """
    Generate human-readable diagnosis using LLM
    
    This converts statistical results into actionable insights
    
    Args:
        drift_results: Drift detection results
        impact_results: Impact analysis results
        timeline: Timeline analysis
        
    Returns:
        LLM diagnosis with explanations and recommendations
    """
    
    # Prepare structured evidence for LLM
    evidence = _prepare_evidence(drift_results, impact_results, timeline)
    
    # Generate diagnosis prompt
    prompt = _build_diagnosis_prompt(evidence)
    
    # Call LLM (with fallback if API key not available)
    if OPENAI_API_KEY:
        diagnosis_text = _call_openai(prompt, evidence)
    else:
        diagnosis_text = _generate_rule_based_diagnosis(evidence)
    
    # Parse diagnosis into structured format
    diagnosis = {
        "executive_summary": _extract_summary(diagnosis_text, evidence),
        "root_cause_analysis": _extract_root_cause(diagnosis_text, evidence),
        "severity_assessment": timeline.get("summary", {}).get("severity_assessment", "Unknown"),
        "business_impact": _assess_business_impact(evidence),
        "technical_recommendations": _extract_recommendations(diagnosis_text, evidence),
        "full_diagnosis": diagnosis_text
    }
    
    return diagnosis


def _prepare_evidence(drift_results, impact_results, timeline) -> Dict:
    """Prepare structured evidence for LLM"""
    
    # Get top drifted features
    drifted = [d for d in drift_results if d.get("drift", False)]
    top_drift = sorted(drifted, key=lambda x: x.get("drift_score", 0), reverse=True)[:5]
    
    # Get high impact features
    high_impact = [i for i in impact_results if i.get("impact_level") == "High"]
    
    # Get critical features (drift + impact)
    critical = timeline.get("critical_features", [])
    
    evidence = {
        "total_features": len(drift_results),
        "drifted_count": len(drifted),
        "high_impact_count": len(high_impact),
        "critical_count": len(critical),
        "top_drifted_features": [
            {
                "feature": d["feature"],
                "method": d.get("method", "Unknown"),
                "score": d.get("drift_score", 0),
                "severity": d.get("severity", "Unknown")
            } for d in top_drift
        ],
        "critical_features": critical,
        "timeline_events": timeline.get("events", []),
        "overall_severity": timeline.get("summary", {}).get("severity_assessment", "Unknown")
    }
    
    return evidence


def _build_diagnosis_prompt(evidence: Dict) -> str:
    """Build diagnosis prompt for LLM"""
    
    prompt = f"""You are an expert ML reliability engineer performing a post-mortem analysis on a failed ML model.

**EVIDENCE:**

Total Features Analyzed: {evidence['total_features']}
Features with Drift: {evidence['drifted_count']}
High-Impact Features: {evidence['high_impact_count']}
Critical Features (drift + impact): {evidence['critical_count']}

**TOP DRIFTED FEATURES:**
{json.dumps(evidence['top_drifted_features'], indent=2)}

**CRITICAL FEATURES (Root Cause Candidates):**
{json.dumps(evidence['critical_features'], indent=2)}

**TIMELINE EVENTS:**
{json.dumps(evidence['timeline_events'], indent=2)}

**YOUR TASK:**

Provide a comprehensive diagnosis following this structure:

1. **Root Cause**: What caused the model to fail? Be specific about which features are responsible.

2. **Mechanism**: Explain HOW these feature changes led to model degradation.

3. **Severity**: Rate the severity and urgency (Critical/High/Moderate/Low).

4. **Business Impact**: What are the likely business consequences?

5. **Immediate Actions**: What should the team do RIGHT NOW?

6. **Long-term Fixes**: What should be done to prevent this in the future?

7. **Monitoring Recommendations**: What should be monitored going forward?

Write in clear, actionable language. Be specific. Avoid jargon. Think like an engineer explaining to a product manager.
"""
    
    return prompt


def _call_openai(prompt: str, evidence: Dict) -> str:
    """Call OpenAI API for diagnosis"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=OPENAI_API_KEY)
        
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system", 
                    "content": "You are an expert ML reliability engineer specializing in model failure diagnosis."
                },
                {
                    "role": "user", 
                    "content": prompt
                }
            ],
            temperature=0.3,
            max_tokens=1500
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        print(f"OpenAI API call failed: {e}")
        return _generate_rule_based_diagnosis(evidence)


def _generate_rule_based_diagnosis(evidence: Dict) -> str:
    """
    Generate diagnosis using rules (fallback when LLM unavailable)
    
    This is hackathon-safe and still impressive
    """
    critical = evidence.get("critical_features", [])
    top_drift = evidence.get("top_drifted_features", [])
    severity = evidence.get("overall_severity", "Unknown")
    
    # Use the correct count from evidence
    total_drifted = evidence.get("drifted_count", 0)
    total_features = evidence.get("total_features", 0)
    critical_count = evidence.get("critical_count", 0)
    
    diagnosis = f"""
## Model Autopsy Report

### Root Cause Analysis

The model failure is attributed to significant data drift in {critical_count} critical features (out of {total_drifted} total drifted features from {total_features} analyzed).

**Critical Features Identified:**
"""
    
    if critical:
        diagnosis += "\n".join([f"- **{feat}**: Exhibits both distribution drift AND high impact on predictions" for feat in critical[:3]])
    else:
        diagnosis += "\nNo features show combined drift + high impact correlation."
    
    diagnosis += f"""

**Top Drifted Features:**
"""
    
    for feat in top_drift[:3]:
        diagnosis += f"\n- **{feat['feature']}** ({feat['method']}): Drift score = {feat['score']}, Severity = {feat['severity']}"
    
    diagnosis += f"""

### Severity Assessment

**Overall Severity**: {severity}

### Mechanism of Failure

The model was trained on a baseline distribution that no longer represents the current data reality. Key features have experienced:

1. **Distribution Shift**: The statistical properties of input features have changed significantly.
2. **New Data Patterns**: Production data contains patterns not seen during training.
3. **Feature Instability**: Critical features show high variance in production.

This leads to degraded predictions as the model's learned patterns no longer apply.

### Business Impact

- **Prediction Accuracy**: Expected to be degraded proportionally to drift severity
- **User Trust**: Incorrect predictions may erode user confidence
- **Operational Risk**: Decisions based on faulty predictions could lead to business losses

### Immediate Actions Required

"""
    
    if critical:
        diagnosis += f"1. **URGENT**: Retrain the model with recent production data, prioritizing these features: {', '.join(critical[:3])}\n"
        diagnosis += f"2. **INVESTIGATE**: Check data pipelines and feature engineering for: {', '.join(critical[:3])}\n"
    
    diagnosis += """3. **MONITOR**: Set up real-time drift monitoring for critical features
4. **VALIDATE**: Test retrained model on held-out recent data before deployment

### Long-term Preventive Measures

1. **Implement Continuous Monitoring**: Deploy drift detection in production
2. **Automated Retraining**: Set up triggers for automatic retraining when drift exceeds thresholds
3. **Feature Store**: Maintain versioned feature definitions to detect pipeline changes
4. **Data Validation**: Add schema checks and distribution validation in data pipelines
5. **Regular Model Audits**: Schedule monthly model health checks

### Recommended Monitoring

Going forward, monitor these features closely:
"""
    
    for feat in top_drift[:5]:
        diagnosis += f"- {feat['feature']} (current drift score: {feat['score']})\n"
    
    diagnosis += """
Set alerts for:
- PSI > 0.25 (severe drift)
- KS p-value < 0.01 (highly significant drift)
- New categorical values appearing
- Feature null rate > 10% increase

### Conclusion

This failure is recoverable with prompt action. The root causes are identifiable and addressable through data pipeline investigation and model retraining.
"""
    
    return diagnosis


def _extract_summary(diagnosis_text: str, evidence: Dict) -> str:
    """Extract executive summary"""
    lines = diagnosis_text.split('\n')
    for i, line in enumerate(lines):
        if 'root cause' in line.lower() and i + 1 < len(lines):
            # Get next few lines
            return ' '.join(lines[i+1:i+4]).strip()
    
    return f"Model failure detected in {evidence['critical_count']} critical features with {evidence['overall_severity']} severity."


def _extract_root_cause(diagnosis_text: str, evidence: Dict) -> str:
    """Extract root cause section"""
    if "Root Cause" in diagnosis_text:
        start = diagnosis_text.index("Root Cause")
        end = diagnosis_text.index("###", start + 1) if "###" in diagnosis_text[start+1:] else len(diagnosis_text)
        return diagnosis_text[start:end].strip()
    
    return f"Root cause: Data drift in {evidence['critical_count']} critical features"


def _extract_recommendations(diagnosis_text: str, evidence: Dict) -> List[str]:
    """Extract actionable recommendations"""
    recommendations = []
    
    if "Immediate Actions" in diagnosis_text:
        start = diagnosis_text.index("Immediate Actions")
        end = diagnosis_text.index("###", start + 1) if "###" in diagnosis_text[start+1:] else len(diagnosis_text)
        section = diagnosis_text[start:end]
        
        # Extract numbered or bulleted items
        for line in section.split('\n'):
            if line.strip().startswith(('-', '•', '*')) or any(line.strip().startswith(f"{i}.") for i in range(1, 10)):
                recommendations.append(line.strip())
    
    return recommendations if recommendations else ["Retrain model with recent data", "Monitor critical features"]


def _assess_business_impact(evidence: Dict) -> str:
    """Assess business impact based on evidence"""
    severity = evidence.get("overall_severity", "")
    
    if "CRITICAL" in severity:
        return "HIGH - Immediate business impact likely. Model predictions may be significantly degraded."
    elif "HIGH" in severity:
        return "MODERATE - Noticeable impact on prediction quality expected."
    elif "MODERATE" in severity:
        return "LOW - Minor impact, but trending toward degradation."
    else:
        return "MINIMAL - No significant business impact detected."


def _prepare_evidence_from_prompt(prompt: str) -> Dict:
    """Fallback: extract evidence from prompt if needed"""
    # Simple extraction - in production this would be more robust
    return {
        "critical_features": [],
        "top_drifted_features": [],
        "overall_severity": "Unknown"
    }
