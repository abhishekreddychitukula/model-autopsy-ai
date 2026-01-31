"""
Test script to verify Model Autopsy AI installation
Run this to ensure everything is set up correctly
"""

import sys
import importlib

def test_imports():
    """Test that all required packages are installed"""
    required_packages = [
        'fastapi',
        'uvicorn',
        'pandas',
        'numpy',
        'scipy',
        'sklearn',
        'shap',
        'pydantic'
    ]
    
    print("🔍 Testing package imports...\n")
    
    failed = []
    for package in required_packages:
        try:
            if package == 'sklearn':
                importlib.import_module('sklearn')
            else:
                importlib.import_module(package)
            print(f"✅ {package}")
        except ImportError as e:
            print(f"❌ {package} - {e}")
            failed.append(package)
    
    if failed:
        print(f"\n⚠️  Failed imports: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    else:
        print("\n✅ All packages installed successfully!")
        return True


def test_project_structure():
    """Test that project structure is correct"""
    import os
    
    print("\n🔍 Testing project structure...\n")
    
    required_files = [
        'app/main.py',
        'app/config.py',
        'app/api/routes.py',
        'app/services/data_loader.py',
        'app/services/drift_detection.py',
        'app/services/impact_analysis.py',
        'app/services/timeline.py',
        'app/services/llm_diagnosis.py',
        'app/reports/report_builder.py',
        'app/utils/stats.py',
        'requirements.txt',
        'README.md'
    ]
    
    failed = []
    for file in required_files:
        if os.path.exists(file):
            print(f"✅ {file}")
        else:
            print(f"❌ {file}")
            failed.append(file)
    
    if failed:
        print(f"\n⚠️  Missing files: {', '.join(failed)}")
        return False
    else:
        print("\n✅ All files present!")
        return True


def test_app_import():
    """Test that the app can be imported"""
    print("\n🔍 Testing app import...\n")
    
    try:
        from app.main import app
        print("✅ FastAPI app imported successfully")
        
        from app.services.drift_detection import detect_drift
        print("✅ Drift detection service imported")
        
        from app.services.impact_analysis import analyze_impact
        print("✅ Impact analysis service imported")
        
        from app.services.llm_diagnosis import generate_diagnosis
        print("✅ LLM diagnosis service imported")
        
        print("\n✅ All app modules working!")
        return True
        
    except Exception as e:
        print(f"❌ Error importing app: {e}")
        return False


def test_sample_drift_detection():
    """Test drift detection with sample data"""
    print("\n🔍 Testing drift detection logic...\n")
    
    try:
        import pandas as pd
        import numpy as np
        from app.services.drift_detection import detect_drift
        
        # Create sample data
        np.random.seed(42)
        train_data = pd.DataFrame({
            'feature1': np.random.normal(0, 1, 100),
            'feature2': np.random.choice(['A', 'B', 'C'], 100)
        })
        
        prod_data = pd.DataFrame({
            'feature1': np.random.normal(0.5, 1, 100),  # Shifted mean
            'feature2': np.random.choice(['A', 'B', 'C', 'D'], 100)  # New category
        })
        
        results = detect_drift(train_data, prod_data)
        
        print(f"✅ Drift detection executed successfully")
        print(f"   Features analyzed: {len(results)}")
        print(f"   Drift detected: {sum(1 for r in results if r.get('drift', False))}")
        
        return True
        
    except Exception as e:
        print(f"❌ Drift detection test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("=" * 60)
    print("🔬 Model Autopsy AI - Installation Test")
    print("=" * 60)
    
    results = []
    
    # Test 1: Package imports
    results.append(('Package Imports', test_imports()))
    
    # Test 2: Project structure
    results.append(('Project Structure', test_project_structure()))
    
    # Test 3: App import
    results.append(('App Import', test_app_import()))
    
    # Test 4: Sample drift detection
    results.append(('Drift Detection', test_sample_drift_detection()))
    
    # Summary
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    for test_name, passed in results:
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status} - {test_name}")
    
    all_passed = all(result[1] for result in results)
    
    if all_passed:
        print("\n🎉 All tests passed! You're ready to run Model Autopsy AI!")
        print("\nNext steps:")
        print("1. Generate sample data: python generate_sample_data.py")
        print("2. Start server: uvicorn app.main:app --reload")
        print("3. Visit: http://127.0.0.1:8000/docs")
        return 0
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
