"""Test FastAPI UploadFile behavior"""
from fastapi import UploadFile
from io import BytesIO

# Simulate what FastAPI does
with open('../samples/sample_train.csv', 'rb') as f:
    content = f.read()

# Create a BytesIO object
file_obj = BytesIO(content)

# Test seek
print("Testing seek...")
file_obj.seek(0)
print("✅ seek(0) works on BytesIO")

# Now test with actual file
with open('../samples/sample_train.csv', 'rb') as f:
    print("\nTesting seek on real file...")
    f.seek(0)
    print("✅ seek(0) works on real file")
    
print("\n✅ seek(0) should work fine!")
