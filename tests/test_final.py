"""Comprehensive error test"""
import requests
import json

# Test files
files = {
    'train': ('sample_train.csv', open('../samples/sample_train.csv', 'rb'), 'text/csv'),
    'prod_old': ('sample_prod_old.csv', open('../samples/sample_prod_old.csv', 'rb'), 'text/csv'),
    'prod_new': ('sample_prod_new.csv', open('../samples/sample_prod_new.csv', 'rb'), 'text/csv')
}

print("Testing Model Autopsy API...")
print("=" * 50)

try:
    response = requests.post(
        "http://127.0.0.1:8000/run-autopsy",
        files=files,
        timeout=120
    )
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"\nResponse Body:")
    print("-" * 50)
    
    # Try to parse as JSON
    try:
        data = response.json()
        print(json.dumps(data, indent=2))
        
        if response.status_code == 200:
            print("\n" + "=" * 50)
            print("SUCCESS! Analysis completed.")
            print("=" * 50)
        else:
            print("\n" + "=" * 50)
            print(f"ERROR! Status {response.status_code}")
            print("=" * 50)
    except json.JSONDecodeError:
        print(response.text)
        
except requests.exceptions.Timeout:
    print("ERROR: Request timed out after 120 seconds")
except Exception as e:
    print(f"ERROR: {type(e).__name__}: {str(e)}")
finally:
    for name, (fname, f, ctype) in files.items():
        f.close()
