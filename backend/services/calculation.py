def calculate_bmi(weight: float, height: float) -> float:
    height_m = height / 100
    bmi = weight / (height_m ** 2)
    return round(bmi, 2)



def get_bmi_category(bmi: float) -> str:
    if bmi < 18.5:
        return "Underweight"
    elif bmi < 25:
        return "Normal"
    elif bmi < 30:
        return "Overweight"
    else:
        return "Obese"
    


def feet_inches_to_cm(feet: int, inches: int = 0) -> float:
    total_inches = (feet * 12) + inches
    cm = total_inches * 2.54
    return round(cm, 2)



def calculate_tdee(weight: float, height: float, age: int, gender: str, activity_level: str) -> float:
    if gender == "male":
        bmr = 10 * weight + 6.25 * height - 5 * age + 5
    else:
        bmr = 10 * weight + 6.25 * height - 5 * age - 161

    activity_factors = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725
    }

    tdee = bmr * activity_factors[activity_level]
    return round(tdee, 2)



def get_calorie_targets(tdee: float) -> dict:
    return {
        "cut": round(tdee - 500, 2),
        "maintain": tdee,
        "bulk": round(tdee + 500, 2)
    }