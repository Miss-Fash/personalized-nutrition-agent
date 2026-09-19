import os

from dotenv import load_dotenv
from groq import Groq


# Load environment variables
load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    raise ValueError(
        "GROQ_API_KEY was not found. "
        "Please check your .env file."
    )

client = Groq(api_key=api_key)


def generate_nutrition_advice(profile):

    prompt = f"""
You are the Nutrilead AI Nutrition Adviser.

Provide practical, simple and personalized nutrition guidance
based on the user's profile below.

User profile:
- Age: {profile.get("age")}
- Sex: {profile.get("sex")}
- Height: {profile.get("height")} cm
- Weight: {profile.get("weight")} kg
- Dietary preference: {profile.get("dietary_preference")}
- Health goal: {profile.get("health_goal")}
- Activity level: {profile.get("activity_level")}
- Food allergies: {profile.get("allergies")}
- Foods the user enjoys: {profile.get("preferred_foods")}
- Foods the user wants to avoid: {profile.get("avoided_foods")}

Give:
1. A short personalized nutrition summary.
2. Recommended foods that fit the user's goal.
3. A simple one-day meal suggestion.
4. Practical healthy eating tips.
5. A short Nutrilead tip.

Use simple English.

Do not diagnose diseases or prescribe medication.
If the user's information suggests a medical condition,
recommend speaking with a qualified healthcare professional.

Keep the response practical and easy to understand.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and practical nutrition "
                    "adviser for the Nutrilead application."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content


def generate_meal_plan(profile):

    prompt = f"""
You are the Nutrilead AI Nutrition Adviser.

Create a simple, practical one-day Nigerian-friendly meal plan
based on the user's nutrition profile.

User profile:
- Age: {profile.get("age")}
- Sex: {profile.get("sex")}
- Height: {profile.get("height")} cm
- Weight: {profile.get("weight")} kg
- Dietary preference: {profile.get("dietary_preference")}
- Health goal: {profile.get("health_goal")}
- Activity level: {profile.get("activity_level")}
- Food allergies: {profile.get("allergies")}
- Foods the user enjoys: {profile.get("preferred_foods")}
- Foods the user wants to avoid: {profile.get("avoided_foods")}

Create:

1. Breakfast
2. Mid-morning snack
3. Lunch
4. Afternoon snack
5. Dinner
6. A short hydration tip

Use foods that are realistic and commonly available in Nigeria.

Consider the user's allergies, dietary preference,
health goal, preferred foods, and foods they want to avoid.

Keep the portions practical and the explanation simple.

Do not diagnose diseases or prescribe medication.
If the user's information suggests a medical condition,
recommend speaking with a qualified healthcare professional.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and practical nutrition "
                    "adviser for the Nutrilead application."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_completion_tokens=1000
    )

    return response.choices[0].message.content


def generate_daily_tip(profile):

    prompt = f"""
You are the Nutrilead AI Nutrition Adviser.

Give one short, practical nutrition tip for today.

Consider the user's profile:

- Age: {profile.get("age")}
- Sex: {profile.get("sex")}
- Dietary preference: {profile.get("dietary_preference")}
- Health goal: {profile.get("health_goal")}
- Activity level: {profile.get("activity_level")}
- Food allergies: {profile.get("allergies")}
- Foods they enjoy: {profile.get("preferred_foods")}
- Foods they avoid: {profile.get("avoided_foods")}

The tip should:
- Be practical and easy to apply today.
- Use simple English.
- Be relevant to the user's goal.
- Consider their food preferences and allergies.
- Be no more than 3 short sentences.

Do not diagnose diseases or prescribe medication.
"""

    response = client.chat.completions.create(
        model="openai/gpt-oss-120b",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are a careful and practical nutrition "
                    "adviser for the Nutrilead application."
                )
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        temperature=0.7,
        max_completion_tokens=300
    )

    return response.choices[0].message.content