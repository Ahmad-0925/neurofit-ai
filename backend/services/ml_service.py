import joblib
import pandas as pd
import os

MODEL_PATH = os.path.join(os.path.dirname(__file__), "..", "ml", "model.pkl")
model = joblib.load(MODEL_PATH)

def predict_fitness_score(age: int, weight: float, height: float, bmi: float, tdee: float, activity_level: str):
    activity_map = {"sedentary": 1, "light": 2, "moderate": 3, "active": 4}
    activity_num = activity_map[activity_level]

    input_data = pd.DataFrame([{
        "age": age,
        "weight": weight,
        "height": height,
        "bmi": bmi,
        "tdee": tdee,
        "activity_level": activity_num
    }])

    prediction = model.predict(input_data)[0]
    return round(float(prediction), 2)