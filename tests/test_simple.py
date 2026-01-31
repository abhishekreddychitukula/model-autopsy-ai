"""Simple API test"""
import requests
import json

files = {
    'train': ('train.csv', open('../samples/sample_train.csv', 'rb')),
    'prod_old': ('prod_old.csv', open('../samples/sample_prod_old.csv', 'rb')),
    'prod_new': ('prod_new.csv', open('../samples/sample_prod_new.csv', 'rb'))
}

print("Sending POST to /run-autopsy...")

response = requests.post("http://127.0.0.1:8000/run-autopsy", files=files, timeout=90)

print(f"Status: {response.status_code}")
print(f"Response length: {len(response.text)}")

if response.status_code == 200:
    data = response.json()
    print("SUCCESS!")
    print(json.dumps(data, indent=2)[:500])
else:
    print("FAILED")
    print(response.text[:500])

# Close files
for name, (fname, f) in files.items():
    f.close()
