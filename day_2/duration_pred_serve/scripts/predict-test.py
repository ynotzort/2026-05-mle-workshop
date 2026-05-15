import requests

url = "http://127.0.0.1:8000/predict"
trip_data = {
    "PULocationID": "43",
    "DOLocationID": "238",
    "trip_distance": 1.16
}
response = requests.post(url, json=trip_data).json()
print(response)
