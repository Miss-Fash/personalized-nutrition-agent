import os
import streamlit as st
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

# Get API key from Render environment variable first
api_key = os.getenv("GROQ_API_KEY")

# If not found, try Streamlit secrets for local use
if not api_key:
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except Exception:
        api_key = None

if not api_key:
    raise ValueError("GROQ_API_KEY is not configured.")

client = Groq(api_key=api_key)


def generate_nutrition_advice(profile):
    prompt = f"""
You are a friendly nutrition adviser for Nutrilead.

Give simple, practical, Nigerian-friendly nutrition advice based on the user's profile.

User profile:
Age: {profile.get("age")}
Weight: {profile.get("weight")} kg
Height: {profile.get("height")} cm
Dietary preference: {profile.get("dietary_preference")}
Health goal: {profile.get("health_goal")}
Health condition: {profile.get("health_condition")}

Give:
1. A short summary of the user's nutrition needs.
2. Practical foods they can eat.
3. Foods they may want to reduce.
4. Simple lifestyle tips.

Do not diagnose diseases or prescribe medication.
Use simple English.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a helpful nutrition adviser for Nutrilead."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


def generate_meal_plan(profile):
    prompt = f"""
Create a simple one-day Nigerian-friendly meal plan for this user.

User profile:
Age: {profile.get("age")}
Weight: {profile.get("weight")} kg
Height: {profile.get("height")} cm
Dietary preference: {profile.get("dietary_preference")}
Health goal: {profile.get("health_goal")}
Health condition: {profile.get("health_condition")}

Include:
- Breakfast
- Mid-morning snack
- Lunch
- Afternoon snack
- Dinner
- Water/hydration suggestion

Use affordable and commonly available Nigerian foods where possible.

Keep the meal plan practical and easy to follow.
Do not prescribe medication or claim to treat a disease.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a practical Nigerian nutrition meal-planning assistant for Nutrilead."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content


def generate_daily_tip(profile):
    prompt = f"""
Give one short and practical daily nutrition tip for this user.

User profile:
Age: {profile.get("age")}
Dietary preference: {profile.get("dietary_preference")}
Health goal: {profile.get("health_goal")}
Health condition: {profile.get("health_condition")}

The tip should be simple, realistic and useful in everyday Nigerian life.
Do not diagnose or prescribe medication.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": "You are a friendly nutrition adviser for Nutrilead."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
    )

    return response.choices[0].message.content
  