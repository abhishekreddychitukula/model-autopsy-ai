"""Detailed error test"""
import requests

files = {
    'train': open('../samples/sample_train.csv', 'rb'),
    'prod_old': open('../samples/sample_prod_old.csv', 'rb'),
    'prod_new': open('../samples/sample_prod_new.csv', 'rb')
}

try:
    response = requests.post("http://127.0.0.1:8000/run-autopsy", files=files, timeout=60)
    print(f"Status: {response.status_code}")
    print(f"Headers: {response.headers}")
    print(f"Response: {response.text}")
finally:
    for f in files.values():
        f.close()
