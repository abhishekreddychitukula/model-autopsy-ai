"""Quick API test script"""
import requests
import time

# Wait for server to be ready
time.sleep(2)

# Test health check
print("Testing health check...")
response = requests.get("http://127.0.0.1:8000/")
print(f"Status: {response.status_code}")
print(f"Response: {response.json()}\n")

# Test autopsy endpoint
print("Testing autopsy analysis...")
files = {
    'train': open('../samples/sample_train.csv', 'rb'),
    'prod_old': open('../samples/sample_prod_old.csv', 'rb'),
    'prod_new': open('../samples/sample_prod_new.csv', 'rb')
}

try:
    response = requests.post("http://127.0.0.1:8000/run-autopsy", files=files, timeout=60)
    print(f"Status: {response.status_code}")
    
    if response.status_code == 200:
        result = response.json()
        print("✅ Autopsy analysis successful!")
        print(f"Drift detected in {result['summary']['drift_summary']['total_drifted']} features")
        print(f"High impact features: {result['summary']['impact_summary']['high_impact_count']}")
        print(f"Critical features: {result['timeline']['summary']['critical_features']}")
        print(f"\nDiagnosis: {result['diagnosis']['diagnosis'][:200]}...")
    else:
        print(f"❌ Error: {response.text}")
finally:
    for f in files.values():
        f.close()
