import os
from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from app.schemas import UserInput
from app.gemini_generator import generate_workout_gemini
from app.gemini_flash_generator import generate_nutrition_tip_with_flash
from app.updated_plan import update_workout_plan
from app.database import (save_user, save_plan, update_plan, get_plan_row,
                          get_user, get_all_users, delete_user)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

router = APIRouter()


@router.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse(request, "index.html", {"error": None})


@router.post("/generate-workout", response_class=HTMLResponse)
def generate_workout(
    request: Request,
    username: str = Form(...),
    user_id: str = Form(...),
    age: int = Form(...),
    weight: float = Form(...),
    goal: str = Form(...),
    intensity: str = Form(...),
):
    data = UserInput(username=username, user_id=user_id, age=age,
                     weight=weight, goal=goal, intensity=intensity)
    try:
        plan = generate_workout_gemini(data)
        tip = generate_nutrition_tip_with_flash(data.goal)
    except Exception as e:
        return templates.TemplateResponse(
            request, "index.html", {"error": f"AI error: {e}"}, status_code=502
        )

    save_user(data)
    save_plan(data.user_id, plan, tip)

    return templates.TemplateResponse(request, "result.html", {
        "username": username, "user_id": user_id, "age": age, "weight": weight,
        "goal": goal, "intensity": intensity,
        "workout_plan": plan, "nutrition_tip": tip, "message": None,
    })


@router.post("/submit-feedback", response_class=HTMLResponse)
def submit_feedback(request: Request, user_id: str = Form(...), feedback: str = Form(...)):
    user = get_user(user_id)
    row = get_plan_row(user_id)
    if not user or not row:
        return templates.TemplateResponse(
            request, "index.html", {"error": f"User ID '{user_id}' kedaikkala. Mudhalla plan generate pannunga."},
            status_code=404,
        )

    base_plan = row["updated"] or row["original"]
    try:
        new_plan = update_workout_plan(base_plan, feedback)
    except Exception as e:
        return templates.TemplateResponse(
            request, "index.html", {"error": f"AI error: {e}"}, status_code=502
        )

    update_plan(user_id, new_plan)

    return templates.TemplateResponse(request, "result.html", {
        **user,
        "workout_plan": new_plan, "nutrition_tip": row["tip"],
        "message": "Plan successfully updated based on your feedback!",
    })


@router.get("/view-all-users", response_class=HTMLResponse)
def view_all_users(request: Request):
    return templates.TemplateResponse(request, "all_users.html", {"users": get_all_users()})


@router.post("/delete-user")
def delete_user_route(user_id: str = Form(...)):
    delete_user(user_id)
    return RedirectResponse("/view-all-users", status_code=303)
