import pickle
from typing import Any
from fastapi import FastAPI
from pydantic import BaseModel, Field

model_path = "models/2022-01.bin"

with open(model_path, "rb") as f_in:
    model = pickle.load(f_in)

### server part
class PredictRequest(BaseModel):
    """Inputs required for the prediction."""
    PULocationID: str = Field(description="PickUp location ID")
    DOLocationID: str = Field(description="DropOff location ID")
    trip_distance: float = Field(description="Distance in km")

class PredictionResponse(BaseModel):
    """Predicion result."""
    prediction_duration_minutes: float = Field(description="Predicted trip duration in minutes")

def prepare_features(predict_request: PredictRequest) -> dict[str, Any]:
    result = predict_request.model_dump()
    result["trip_distance"] = float(result["trip_distance"])
    return result

def predict(model_input: dict[str, Any]) -> float:
    prediction = model.predict(model_input)
    return prediction[0]

def post_process_model_output(prediction: float) -> float:
    return prediction

app = FastAPI()

@app.post("/predict")
def predict_endpoint(predict_request: PredictRequest) -> PredictionResponse:
    model_input = prepare_features(predict_request)
    prediction_raw = predict(model_input)
    prediction = post_process_model_output(prediction_raw)
    result = PredictionResponse(prediction_duration_minutes=prediction)
    return result

# trip_data = {
#     "PULocationID": "43",
#     "DOLocationID": "238",
#     "trip_distance": 1.16
# }
# prediction = model.predict(trip_data)[0]
# print(prediction)
