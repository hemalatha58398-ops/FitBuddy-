import os
from sqlalchemy import create_engine, Column, Integer, String, Float, Text
from sqlalchemy.orm import declarative_base, sessionmaker

ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(ROOT_DIR, "fitbuddy.db")

engine = create_engine(f"sqlite:///{DB_PATH}", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(bind=engine, autoflush=False)
Base = declarative_base()


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, unique=True, index=True, nullable=False)
    username = Column(String, nullable=False)
    age = Column(Integer)
    weight = Column(Float)
    goal = Column(String)
    intensity = Column(String)


class Plan(Base):
    __tablename__ = "plans"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(String, index=True, nullable=False)
    original_plan = Column(Text)
    updated_plan = Column(Text)
    nutrition_tip = Column(Text)


def save_user(data):
    db = SessionLocal()
    try:
        user = db.query(User).filter(User.user_id == data.user_id).first()
        if user is None:
            user = User(user_id=data.user_id)
            db.add(user)
        user.username = data.username
        user.age = data.age
        user.weight = data.weight
        user.goal = data.goal
        user.intensity = data.intensity
        db.commit()
    finally:
        db.close()


def save_plan(user_id, plan, tip):
    db = SessionLocal()
    try:
        row = db.query(Plan).filter(Plan.user_id == user_id).first()
        if row is None:
            row = Plan(user_id=user_id)
            db.add(row)
        row.original_plan = plan
        row.updated_plan = None
        row.nutrition_tip = tip
        db.commit()
    finally:
        db.close()


def update_plan(user_id, new_plan):
    db = SessionLocal()
    try:
        row = db.query(Plan).filter(Plan.user_id == user_id).first()
        if row:
            row.updated_plan = new_plan
            db.commit()
    finally:
        db.close()


def get_original_plan(user_id):
    db = SessionLocal()
    try:
        row = db.query(Plan).filter(Plan.user_id == user_id).first()
        return row.original_plan if row else None
    finally:
        db.close()


def get_plan_row(user_id):
    db = SessionLocal()
    try:
        row = db.query(Plan).filter(Plan.user_id == user_id).first()
        if not row:
            return None
        return {"original": row.original_plan, "updated": row.updated_plan, "tip": row.nutrition_tip}
    finally:
        db.close()


def get_user(user_id):
    db = SessionLocal()
    try:
        u = db.query(User).filter(User.user_id == user_id).first()
        if not u:
            return None
        return {"username": u.username, "user_id": u.user_id, "age": u.age,
                "weight": u.weight, "goal": u.goal, "intensity": u.intensity}
    finally:
        db.close()


def get_all_users():
    db = SessionLocal()
    try:
        result = []
        for u in db.query(User).all():
            p = db.query(Plan).filter(Plan.user_id == u.user_id).first()
            result.append({
                "username": u.username, "user_id": u.user_id, "age": u.age,
                "weight": u.weight, "goal": u.goal, "intensity": u.intensity,
                "original_plan": p.original_plan if p else "",
                "updated_plan": p.updated_plan if p else "",
            })
        return result
    finally:
        db.close()


def delete_user(user_id):
    db = SessionLocal()
    try:
        db.query(Plan).filter(Plan.user_id == user_id).delete()
        db.query(User).filter(User.user_id == user_id).delete()
        db.commit()
    finally:
        db.close()
