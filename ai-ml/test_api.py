import requests
import json

# Test the root endpoint
response = requests.get('http://localhost:8000/', headers={'Authorization': 'Bearer admin_key'})
print("Root endpoint:", response.status_code)
print(json.dumps(response.json(), indent=2))

# Test the historical predictions endpoint
response = requests.get('http://localhost:8000/api/historical/predictions/profitability_prediction?days=7', 
                       headers={'Authorization': 'Bearer admin_key'})
print("\nHistorical predictions endpoint:", response.status_code)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(response.text)

# Test the retraining triggers endpoint
response = requests.get('http://localhost:8000/api/retraining/triggers/profitability_prediction', 
                       headers={'Authorization': 'Bearer admin_key'})
print("\nRetraining triggers endpoint:", response.status_code)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(response.text)

# Test the reporting endpoint
response = requests.get('http://localhost:8000/api/reporting/performance/summary?days=30', 
                       headers={'Authorization': 'Bearer admin_key'})
print("\nPerformance summary endpoint:", response.status_code)
if response.status_code == 200:
    print(json.dumps(response.json(), indent=2))
else:
    print(response.text)