"""Pydantic schemas for request/response validation"""
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
from datetime import datetime

class DriftResult(BaseModel):
    """Schema for drift detection result"""
    feature: str
    method: str
    drift: bool
    drift_score: float
    severity: str
    statistics: Optional[Dict] = None
    
class ImpactResult(BaseModel):
    """Schema for impact analysis result"""
    feature: str
    impact_score: float
    impact_level: str
    metrics: Optional[Dict] = None
    statistics: Optional[Dict] = None

class TimelineEvent(BaseModel):
    """Schema for timeline event"""
    event_type: str
    severity: str
    description: str
    features: List[str]
    timestamp: str
    explanation: Optional[str] = None

class Diagnosis(BaseModel):
    """Schema for LLM diagnosis"""
    executive_summary: str
    root_cause_analysis: str
    severity_assessment: str
    business_impact: str
    technical_recommendations: List[str]
    full_diagnosis: str

class AutopsyReport(BaseModel):
    """Complete autopsy report schema"""
    metadata: Dict
    executive_summary: Dict
    drift_analysis: Dict
    impact_analysis: Dict
    timeline: Dict
    diagnosis: Dict
    recommendations: Dict
    visualizations: Optional[Dict] = None

class UploadResponse(BaseModel):
    """Response schema for file upload"""
    status: str
    message: str
    files_received: List[str]

class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    message: str
