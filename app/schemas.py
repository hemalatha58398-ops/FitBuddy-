from pydantic import BaseModel, Field


class UserInput(BaseModel):
    username: str
    user_id: str
    age: int = Field(ge=10, le=100)
    weight: float = Field(gt=20, lt=400)
    goal: str
    intensity: str


class FeedbackRequest(BaseModel):
    user_id: str
    feedback: str
