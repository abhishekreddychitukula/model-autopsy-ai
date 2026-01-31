"""Direct test of the analysis functions"""
import pandas as pd
import sys
import traceback

# Import the services
from app.services.data_loader import load_and_validate
from app.services.drift_detection import detect_drift
from app.services.impact_analysis import analyze_impact
from app.services.timeline import build_timeline
from app.services.llm_diagnosis import generate_diagnosis
from app.reports.report_builder import build_report

# Create mock file objects
class MockFile:
    def __init__(self, filepath):
        self.filepath = filepath
        self.file = open(filepath, 'rb')

try:
    print("Step 1: Loading data...")
    train_file = MockFile('sample_train.csv')
    old_file = MockFile('sample_prod_old.csv')
    new_file = MockFile('sample_prod_new.csv')
    
    train_df, old_df, new_df = load_and_validate(train_file, old_file, new_file)
    print(f"✅ Data loaded: train={len(train_df)}, old={len(old_df)}, new={len(new_df)}")
    
    print("\nStep 2: Detecting drift...")
    drift_results = detect_drift(train_df, new_df)
    print(f"✅ Drift detected in {sum(1 for d in drift_results if d['drift'])} out of {len(drift_results)} features")
    
    print("\nStep 3: Analyzing impact...")
    impact_results = analyze_impact(train_df, old_df, new_df)
    print(f"✅ Impact analyzed for {len(impact_results)} features")
    
    print("\nStep 4: Building timeline...")
    timeline = build_timeline(drift_results, impact_results)
    print(f"✅ Timeline built with {len(timeline['events'])} events")
    print(f"   Critical features: {timeline.get('critical_features', [])}")
    
    print("\nStep 5: Generating diagnosis...")
    diagnosis = generate_diagnosis(drift_results, impact_results, timeline)
    print(f"✅ Diagnosis generated")
    print(f"   Keys: {list(diagnosis.keys())}")
    if 'executive_summary' in diagnosis:
        print(f"   Executive summary: {diagnosis['executive_summary'][:100]}...")
    if 'full_diagnosis' in diagnosis:
        print(f"   Full diagnosis length: {len(diagnosis['full_diagnosis'])} chars")
    
    print("\nStep 6: Building report...")
    report = build_report(drift_results, impact_results, timeline, diagnosis)
    print(f"✅ Report built successfully")
    print(f"\n📊 Summary:")
    print(f"   Report keys: {list(report.keys())}")
    if 'drift_analysis' in report:
        print(f"   Total drifted features: {report['drift_analysis']['summary']['drifted_features_count']}")
    if 'impact_analysis' in report:
        print(f"   High impact features: {report['impact_analysis']['summary']['high_impact_count']}")
    
except Exception as e:
    print(f"\n❌ Error occurred:")
    print(f"   {type(e).__name__}: {str(e)}")
    print(f"\n{traceback.format_exc()}")
    sys.exit(1)
finally:
    try:
        train_file.file.close()
        old_file.file.close()
        new_file.file.close()
    except:
        pass
