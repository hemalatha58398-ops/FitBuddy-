from app.gemini_client import ask_gemini, PRO_MODEL


def update_workout_plan(original_plan: str, feedback: str) -> str:
    prompt = f"""
You are a professional fitness coach. Below is a user's current 7-day workout plan
and their feedback. Revise the plan to apply the feedback.

CURRENT PLAN:
{original_plan}

USER FEEDBACK:
{feedback}

Rules:
- Keep the same Day 1 to Day 7 format (Focus, Warm-up, Main workout, Cooldown).
- Return the full updated plan in plain text only. No markdown symbols.
"""
    return ask_gemini(PRO_MODEL, prompt)
