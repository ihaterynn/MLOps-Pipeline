import sys
import os

# Get the absolute path of the parent directory (backend)
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pytest
from fastapi.testclient import TestClient
from main import app  # Now, we can import main.py correctly

client = TestClient(app)

# ✅ 1. Test if the homepage is reachable
def test_homepage():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]  # Ensure HTML response

# ✅ 2. Test the predict endpoint (dummy text-based inference)
def test_predict():
    input_data = {"input_data": "Hello ML"}
    response = client.post("/predict", json=input_data)
    assert response.status_code == 200
    json_data = response.json()
    # Adjust this assertion if your dummy logic changes
    assert "prediction" in json_data
    assert "Hello ML" in json_data["prediction"]

# ✅ 3. Test the image inference endpoint using a sample image
def test_predict_image():
    # Path to the sample image relative to this test file
    image_path = os.path.join(os.path.dirname(__file__), "data", "9.jpg")
    
    # Open the file in binary mode and send it as part of the request
    with open(image_path, "rb") as image_file:
        response = client.post(
            "/predict_image",
            files={"file": ("9.jpg", image_file, "image/jpeg")}
        )
    assert response.status_code == 200
    json_data = response.json()
    # Check that the prediction key is present and that it is an integer
    assert "prediction" in json_data
    assert isinstance(json_data["prediction"], int)
