"""API routes for Model Autopsy AI"""
from fastapi import APIRouter, UploadFile, File, HTTPException
from typing import Optional
import traceback

from app.services.data_loader import load_and_validate
from app.services.drift_detection import detect_drift
from app.services.impact_analysis import analyze_impact
from app.services.timeline import build_timeline
from app.services.llm_diagnosis import generate_diagnosis
from app.reports.report_builder import build_report

router = APIRouter()

@router.get("/test")
def test_endpoint():
    """Simple test endpoint"""
    return {"status": "Backend is working!", "test": "success"}

@router.post("/run-autopsy")
async def run_autopsy(
    train: UploadFile = File(..., description="Training data (baseline)"),
    prod_old: UploadFile = File(..., description="Production data (before failure)"),
    prod_new: UploadFile = File(..., description="Production data (after failure)"),
    predictions: Optional[UploadFile] = File(None, description="Optional: predictions for SHAP analysis")
):
    """
    Run complete autopsy analysis on ML model failure
    
    This endpoint performs:
    1. Data validation
    2. Drift detection (KS-Test, PSI, Chi-Square)
    3. Feature impact analysis
    4. Timeline reconstruction
    5. LLM-powered diagnosis
    
    Returns a comprehensive autopsy report with actionable insights.
    """
    # Log immediately
    with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "w") as f:
        f.write("Function was called!\n")
    
    try:
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("Inside try block\n")
        
        print("\n=== AUTOPSY REQUEST RECEIVED ===")
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("After first print\n")
        
        print("Step 1: Loading and validating data...")
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("About to call load_and_validate\n")
        
        # Step 1: Load and validate data (async now)
        train_df, old_df, new_df = await load_and_validate(train, prod_old, prod_new)
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write(f"Data loaded: {len(train_df)} rows\n")
        print(f"✅ Data loaded: train={len(train_df)}, old={len(old_df)}, new={len(new_df)}")
        
        print("Step 2: Detecting drift...")
        # Step 2: Detect drift across features
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("About to detect drift\n")
        drift_results = detect_drift(train_df, new_df)
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write(f"Drift detected: {len(drift_results)} features\n")
        print(f"Drift detection complete: {len(drift_results)} features analyzed")
        
        print("Step 3: Analyzing impact...")
        # Step 3: Analyze feature impact
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("About to analyze impact\n")
        impact_results = analyze_impact(train_df, old_df, new_df)
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write(f"Impact analyzed: {len(impact_results)} features\n")
        print(f"Impact analysis complete: {len(impact_results)} features")
        
        print("Step 4: Building timeline...")
        # Step 4: Build failure timeline
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("About to build timeline\n")
        timeline = build_timeline(drift_results, impact_results)
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("Timeline built\n")
        print("Timeline built successfully")
        
        print("Step 5: Generating diagnosis...")
        # Step 5: Generate LLM diagnosis
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("About to generate diagnosis\n")
        diagnosis = generate_diagnosis(drift_results, impact_results, timeline)
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("Diagnosis generated\n")
        print("Diagnosis generated")
        
        print("Step 6: Building report...")
        # Step 6: Build comprehensive report
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("About to build report\n")
        report = build_report(drift_results, impact_results, timeline, diagnosis)
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("Report built - SUCCESS!\n")
        print("Report built successfully")
        
        with open("c:\\Users\\Abhishek  Reddy . C\\OneDrive\\Desktop\\k\\model-autopsy-ai\\function_called.txt", "a") as f:
            f.write("About to return report\\n")
            f.write(f"Report keys: {list(report.keys())}\\n")
        
        # Convert to JSON-serializable format (handles NumPy/Pandas types)
        import json
        json_report = json.loads(json.dumps(report, default=str))
        
        return json_report
        
    except ValueError as e:
        error_msg = f"ValueError: {str(e)}"
        print(error_msg)
        with open("backend.log", "a") as f:
            f.write(f"ValueError: {error_msg}\n")
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        error_detail = f"Autopsy failed: {str(e)}\n{traceback.format_exc()}"
        print(error_detail)
        with open("backend.log", "a") as f:
            f.write(f"Exception: {error_detail}\n")
        raise HTTPException(status_code=500, detail=error_detail)

@router.post("/analyze-drift")
async def analyze_drift_only(
    train: UploadFile = File(...),
    production: UploadFile = File(...)
):
    """Quick drift analysis without full autopsy"""
    try:
        train_df, _, prod_df = await load_and_validate(train, production, production)
        drift_results = detect_drift(train_df, prod_df)
        
        return {
            "status": "success",
            "drift_detected": any(d["drift"] for d in drift_results),
            "results": drift_results
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
