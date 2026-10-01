from app.gemini_client import ask_gemini, FLASH_MODEL


def generate_nutrition_tip_with_flash(goal: str) -> str:
    prompt = f"""
Give one concise, practical nutrition or recovery tip (2-3 sentences) for someone
whose fitness goal is: {goal}. Plain text only, no markdown.
"""
    return ask_gemini(FLASH_MODEL, prompt)
