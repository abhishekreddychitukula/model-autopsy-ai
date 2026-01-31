"""Test with detailed error output"""
import requests
import json

files = {
    'train': ('train.csv', open('../samples/sample_train.csv', 'rb'), 'text/csv'),
    'prod_old': ('prod_old.csv', open('../samples/sample_prod_old.csv', 'rb'), 'text/csv'),
    'prod_new': ('prod_new.csv', open('../samples/sample_prod_new.csv', 'rb'), 'text/csv')
}

try:
    print("Sending request to http://127.0.0.1:8000/run-autopsy...")
    response = requests.post("http://127.0.0.1:8000/run-autopsy", files=files, timeout=60)
    
    print(f"\nStatus Code: {response.status_code}")
    print(f"Headers: {dict(response.headers)}")
    print(f"\nResponse Text:")
    print(response.text)
    
    if response.status_code == 200:
        data = response.json()
        print("\n✅ SUCCESS!")
        print(json.dumps(data, indent=2)[:500])
    else:
        print(f"\n❌ ERROR {response.status_code}")
        try:
            error_data = response.json()
            print(json.dumps(error_data, indent=2))
        except:
            print(response.text)
            
except Exception as e:
    print(f"\n❌ Exception: {e}")
    import traceback
    traceback.print_exc()
finally:
    for _, f_tuple in files.items():
        f_tuple[1].close()
