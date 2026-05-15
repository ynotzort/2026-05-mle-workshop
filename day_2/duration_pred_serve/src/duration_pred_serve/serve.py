import pickle

model_path = "models/2022-01.bin"

with open(model_path, "rb") as f_in:
    model = pickle.load(f_in)

trip_data = {
    "PULocationID": "43",
    "DOLocationID": "238",
    "trip_distance": 1.16
}
prediction = model.predict(trip_data)[0]
print(prediction)
