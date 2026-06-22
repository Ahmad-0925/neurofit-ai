import joblib
import pandas as pd
import os
import shap

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

def explain_prediction(age: int, weight: float, height: float, bmi: float, tdee: float, activity_level: str):
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

    preprocessor = model.named_steps["preprocessor"]
    regressor = model.named_steps["model"]

    transformed_input = preprocessor.transform(input_data)

    explainer = shap.TreeExplainer(regressor)
    shap_values = explainer.shap_values(transformed_input)

    feature_names = ["age", "weight", "height", "bmi", "tdee", "activity_level"]
    
    explanation = []
    for name, value in zip(feature_names, shap_values[0]):
        explanation.append({
            "feature": name,
            "impact": round(float(value), 2)
        })

    explanation.sort(key=lambda x: abs(x["impact"]), reverse=True)
    return explanation