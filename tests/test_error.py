"""Better error test using requests with error capture"""
import requests
import json

files = {
    'train': ('train.csv', open('../samples/sample_train.csv', 'rb'), 'text/csv'),
    'prod_old': ('prod_old.csv', open('../samples/sample_prod_old.csv', 'rb'), 'text/csv'),
    'prod_new': ('prod_new.csv', open('../samples/sample_prod_new.csv', 'rb'), 'text/csv')
}

try:
    print("Sending request to backend...")
    response = requests.post(
        "http://127.0.0.1:8000/run-autopsy",
        files=files,
        timeout=90
    )
    
    print(f"\n=== Response ===")
    print(f"Status: {response.status_code}")
    print(f"Content-Type: {response.headers.get('content-type', 'unknown')}")
    
    # Try to parse as JSON first
    try:
        data = response.json()
        print(f"\n=== JSON Response ===")
        print(json.dumps(data, indent=2)[:500])
    except:
        print(f"\n=== Text Response ===")
        print(response.text[:1000])
        
except requests.exceptions.Timeout:
    print("Request timed out after 90 seconds")
except Exception as e:
    print(f"Error: {type(e).__name__}: {str(e)}")
finally:
    # Close all files
    for name, (fname, f, ctype) in files.items():
        f.close()
