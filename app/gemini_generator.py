from app.gemini_client import ask_gemini, PRO_MODEL
from app.schemas import UserInput


def generate_workout_gemini(user: UserInput) -> str:
    prompt = f"""
You are a professional fitness coach. Create a personalized 7-day workout plan.

User details:
- Name: {user.username}
- Age: {user.age}
- Weight: {user.weight} kg
- Goal: {user.goal}
- Preferred intensity: {user.intensity}

Rules:
- Format as Day 1 to Day 7.
- For each day give: Focus, Warm-up (5-10 mins), Main workout (exercise, sets x reps, rest), Cooldown/recovery tip.
- Include at least one rest or light recovery day.
- Use plain text only. No markdown symbols like ** or #.
"""
    return ask_gemini(PRO_MODEL, prompt)
