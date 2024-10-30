import requests
import os

# Load API URL and key from environment variables
BACKEND_URL = os.getenv("BACKEND_URL")
API_KEY = os.getenv("API_KEY")

# Fetch data from backend
response = requests.get(f"{BACKEND_URL}/data", headers={"Authorization": API_KEY})
print("Data from back-end:", response.json())

# Update data on backend
new_data = "Updated Data"
response = requests.post(f"{BACKEND_URL}/data", json={"data": new_data}, headers={"Authorization": API_KEY})
print("Response after update:", response.json())
