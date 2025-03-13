import openai
import os
from dotenv import load_dotenv

# Initialize environment
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# ----------------------
# SLEEP AGENT
# ----------------------
def sleep_agent(sleep_hours, sleep_quality):
    prompt = f"""
    User slept {sleep_hours} hours last night and rates sleep quality as {sleep_quality}/10.
    Analyze and provide recommendations. Include:
    - Sleep quality assessment
    - Health implications
    - 3 actionable tips for improvement
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a sleep specialist with 20 years experience."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("❌ Error during sleep analysis:", e)
        return f"""🧠 **MOCK Sleep Analysis**
- You slept for {sleep_hours} hours with a quality rating of {sleep_quality}/10.
- This indicates moderate sleep. Less than 7 hours or low quality may lead to fatigue and low focus.
- ✅ **Tips**:
  1. Set a regular sleep schedule.
  2. Avoid screens 1 hour before bed.
  3. Try relaxation techniques like meditation.
"""

# ----------------------
# BMI AGENT
# ----------------------
def bmi_agent(weight_kg, height_cm):
    height_m = height_cm / 100
    bmi = weight_kg / (height_m ** 2)

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a certified nutritionist. Analyze BMI and provide health recommendations."},
                {"role": "user", "content": f"BMI: {bmi:.1f}. Categorize and advise on:"}
            ]
        )
        analysis = response['choices'][0]['message']['content']
        return f"BMI Result: {bmi:.1f}\n{analysis}"
    except Exception as e:
        print("❌ Error during BMI analysis:", e)
        # Mock BMI interpretation
        if bmi < 18.5:
            category = "Underweight"
        elif bmi < 24.9:
            category = "Normal weight"
        elif bmi < 29.9:
            category = "Overweight"
        else:
            category = "Obese"

        return f"""🧠 **MOCK BMI Result: {bmi:.1f} ({category})**
- Keep a balanced diet and regular exercise.
- Focus on long-term sustainable health goals.
"""

# ----------------------
# NUTRITION AGENT
# ----------------------
def nutrition_agent(calorie_intake, dietary_preference, health_goal):
    prompt = f"""
    User has a daily calorie intake of {calorie_intake} calories, prefers {dietary_preference} diet, and aims to {health_goal}.
    Provide a detailed nutrition plan including:
    - Recommended meals for the day
    - Macronutrient breakdown (carbs, proteins, fats)
    - Tips to achieve the health goal
    """
    
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a certified nutritionist with expertise in meal planning."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        print("❌ Error during nutrition planning:", e)
        return f"""🥗 **MOCK Nutrition Plan**
- Calorie Target: {calorie_intake} kcal | Diet: {dietary_preference} | Goal: {health_goal}
- 🍽️ **Meals**: 
  - Breakfast: Oats with fruits
  - Lunch: Quinoa salad with lentils
  - Dinner: Stir-fried veggies with tofu
- ⚖️ **Macronutrients**:
  - Carbs: 50%
  - Proteins: 30%
  - Fats: 20%
- ✅ Stay hydrated and track your portions daily.
"""

# ----------------------
# INPUT VALIDATION
# ----------------------
def get_float_input(prompt):
    while True:
        try:
            return float(input(prompt).strip())
        except ValueError:
            print("Invalid input! Please enter a number.")

def get_int_input(prompt, min_value=None, max_value=None):
    while True:
        try:
            value = int(input(prompt).strip())
            if min_value is not None and value < min_value or max_value is not None and value > max_value:
                print(f"Please enter a value between {min_value} and {max_value}.")
            else:
                return value
        except ValueError:
            print("Invalid input! Please enter an integer.")

# ----------------------
# DASHBOARD INTERFACE
# ----------------------
def health_dashboard():
    print("\n" + "="*40)
    print("  HEALTH AGENT SYSTEM")
    print("="*40)
    print("1. Sleep Analysis")
    print("2. BMI Calculator")
    print("3. Nutrition Planner")
    print("4. Exit")

    while True:
        choice = input("\nChoose option (1-4): ")

        if choice == "1":
            hours = get_float_input("Enter sleep hours: ")
            quality = get_int_input("Rate sleep quality (1-10): ", 1, 10)
            print("\n" + "-"*40)
            print(sleep_agent(hours, quality))
            print("-"*40)

        elif choice == "2":
            weight = get_float_input("Enter weight (kg): ")
            height = get_float_input("Enter height (cm): ")
            print("\n" + "-"*40)
            print(bmi_agent(weight, height))
            print("-"*40)

        elif choice == "3":
            calories = get_float_input("Enter daily calorie intake: ")
            diet = input("Enter dietary preference (e.g., vegetarian, vegan, keto): ").strip()
            goal = input("Enter health goal (e.g., lose weight, gain muscle): ").strip()
            print("\n" + "-"*40)
            print(nutrition_agent(calories, diet, goal))
            print("-"*40)

        elif choice == "4":
            print("Exiting system...")
            break
        else:
            print("Invalid choice! Please try again.")

# ----------------------
# MAIN
# ----------------------
if __name__ == "__main__":
    health_dashboard()
