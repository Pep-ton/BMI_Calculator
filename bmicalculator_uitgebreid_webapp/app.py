from flask import Flask, render_template, request

app = Flask(__name__)

def calculate_bmi(weight, height):
    bmi = weight / ((height / 100) ** 2)
    if bmi < 18.5:
        category = "Underweight"
    elif bmi < 25:
        category = "Normal"
    elif bmi < 30:
        category = "Overweight"
    else:
        category = "Obesity"
    return round(bmi, 2), category

def calculate_bmr(weight, height, age, gender):
    if gender == "man":
        return round((10 * weight) + (6.25 * height) - (5 * age) + 5, 2)
    elif gender == "vrouw":
        return round((10 * weight) + (6.25 * height) - (5 * age) - 161, 2)
    return None

def calculate_tdee(bmr, activity_level):
    factors = {"1": 1.2, "2": 1.375, "3": 1.55, "4": 1.725, "5": 1.9}
    return round(bmr * factors.get(activity_level, 1.2), 2)

def calculate_macros(calories, diet_type):
    if diet_type == "high_protein":
        protein = (calories * 0.4) / 4
        carbs = (calories * 0.3) / 4
        fats = (calories * 0.3) / 9
    elif diet_type == "low_carb":
        protein = (calories * 0.3) / 4
        carbs = (calories * 0.2) / 4
        fats = (calories * 0.5) / 9
    elif diet_type == "low_fat":
        protein = (calories * 0.3) / 4
        carbs = (calories * 0.5) / 4
        fats = (calories * 0.2) / 9
    else:  # Gebalanceerd
        protein = (calories * 0.3) / 4
        carbs = (calories * 0.4) / 4
        fats = (calories * 0.3) / 9
    return round(protein, 2), round(carbs, 2), round(fats, 2)

@app.route('/', methods=['GET', 'POST'])
def index():
    result = {}
    if request.method == 'POST':
        try:
            weight = float(request.form['weight'])
            height = float(request.form['height'])
            age = int(request.form.get('age', 0))
            gender = request.form.get('gender', '').strip().lower()
            activity_level = request.form.get('activity', '1')
            kcal_intake = float(request.form.get('kcal_intake', 0))
            weight_goal = request.form.get('weight_goal', '')
            diet_type = request.form.get('diet_type', 'balanced')
            
            bmi, category = calculate_bmi(weight, height)
            bmr = calculate_bmr(weight, height, age, gender)
            tdee = calculate_tdee(bmr, activity_level) if bmr else None
            kcal_advice = tdee if weight_goal == '' else (tdee - 500 if weight_goal == 'afvallen' else tdee + 500)
            protein, carbs, fats = calculate_macros(kcal_advice, diet_type)
            
            result = {
                "bmi": bmi,
                "category": category,
                "bmr": bmr,
                "tdee": tdee,
                "kcal_advice": kcal_advice,
                "protein": protein,
                "carbs": carbs,
                "fats": fats,
                "weight_goal": weight_goal
            }
        except ValueError:
            result['error'] = "Ongeldige invoer. Probeer opnieuw."
    return render_template('index.html', result=result)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
